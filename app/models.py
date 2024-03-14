import sqlalchemy
from pydantic import BaseModel



class Task(BaseModel):
    id: int

    text: str
    sentiment_label: str
    sentiment_score: float