from fastapi import APIRouter
from service import company_poll_service

router = APIRouter(
    prefix="/poll/company",
    tags=["company_poll"]
)


@router.get("/each_answer_by_question/{question_id}")
async def get_count_of_each_optional_answer_by_id(question_id: int):
    results = await company_poll_service.get_count_of_each_optional_answer_by_id(question_id)
    return results


@router.get("/total_answer_by_question/{question_id}")
async def get_total_answer_count_by_id_question(question_id: int):
    answers_count = await company_poll_service.get_total_answer_count_by_id_question(question_id)
    return {"message": f"there are: {answers_count} answers to question id: {question_id}"}


@router.get("/each_answer_by_user/{user_id}")
async def get_each_answer_by_user_id(user_id: int):
    answers = await company_poll_service.get_each_answer_by_user_id(user_id)
    return answers


@router.get("/total_answer_count_by_user/{user_id}")
async def get_total_answer_count_by_user_id(user_id: int):
    answer_count = await company_poll_service.get_total_answer_count_by_user_id(user_id)
    return {"message": f'The user has answered: {answer_count} questions so far'}


@router.get("/")
async def get_all():
    all_questions_data = await company_poll_service.get_all()
    return all_questions_data
