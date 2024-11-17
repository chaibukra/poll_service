from typing import Optional
from pydantic import BaseModel


class UserAnswer(BaseModel):
    id: Optional[int] = None
    answer_id: int
    user_id: int
