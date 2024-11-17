from typing import Optional
from pydantic import BaseModel


class OptionalAnswer(BaseModel):
    answer_id: Optional[int] = None
    question_id: Optional[int]
    optional_answer_text: str
