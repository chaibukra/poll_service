from pydantic import BaseModel
from model.optional_answer import OptionalAnswer
from model.question import Question


class QuestionRequest(BaseModel):
    question: Question
    option_1: OptionalAnswer
    option_2: OptionalAnswer
    option_3: OptionalAnswer
    option_4: OptionalAnswer
