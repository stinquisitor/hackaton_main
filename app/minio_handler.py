import os
import io
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from minio import Minio
from minio.error import InvalidResponseError as ResponseError

load_dotenv()


app = FastAPI()
client = Minio(
    endpoint=os.getenv('MINIO_ENDPOINT'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)


@app.get("/")
async def index():
    return {"message": "Welcome to the Minio file upload/download app!"}


@app.get("/uploadfile/")
async def upload_form():
    html_content = """
        <html>
            <head>
                <title>Upload File</title>
            </head>
            <body>
                <h1>Upload File</h1>
                <form action="/uploadfile/" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <br><br>
                    <button type="submit">Upload</button>
                </form>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        value_as_bytes = await file.read()

        bucket_name = "my-bucket"
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully!")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

        value_as_a_stream = io.BytesIO(value_as_bytes)

        client.put_object(bucket_name, file.filename, value_as_a_stream, length=len(value_as_bytes))
        return {"message": f"File {file.filename} uploaded successfully."}
    except ResponseError as err:
        return {"error": str(err)}