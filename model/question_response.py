from pydantic import BaseModel
from model.question import Question


class QuestionResponse(BaseModel):
    question: Question
    optional_answer_1_id: int
    optional_answer_1_text: str
    optional_answer_2_id: int
    optional_answer_2_text: str
    optional_answer_3_id: int
    optional_answer_3_text: str
    optional_answer_4_id: int
    optional_answer_4_text: str
