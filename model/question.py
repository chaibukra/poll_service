from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    question_id: Optional[int] = None
    title: str
