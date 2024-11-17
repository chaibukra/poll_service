from fastapi import APIRouter
from starlette import status
from model.question_response import QuestionResponse
from model.user_answer import UserAnswer
from service import user_answer_service

router = APIRouter(
    prefix="/poll/user",
    tags=["user_poll"]
)


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question_by_id(question_id: int):
    return await user_answer_service.get_question_by_id(question_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_answer(user_answer: UserAnswer):
    await user_answer_service.create_user_answer(user_answer)
    return {"message": "User answer created successfully"}


@router.put("/{question_id}")
async def update_user_answer(question_id, user_answer: UserAnswer):
    await user_answer_service.update_user_answer(question_id, user_answer)
    return {"message": f'User answer successfully updated - the new choice for question id:{question_id} is answer id:{user_answer.answer_id}'}


@router.delete("/{user_id}")
async def delete_all_user_answers_by_user_id(user_id: int):
    await user_answer_service.delete_all_user_answers_by_user_id(user_id)
