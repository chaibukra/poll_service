from fastapi import HTTPException
from model.question_request import QuestionRequest
from model.question_response import QuestionResponse
from repository import question_repository, optional_answer_repository
from service import user_answer_service


async def create_question(question: QuestionRequest) -> int:
    question_id = await question_repository.create_question(question.question)
    optional_answers = [question.option_1, question.option_2, question.option_3, question.option_4]
    for optional_answer in optional_answers:
        optional_answer.question_id = question_id
        await optional_answer_repository.create_optional_answer(optional_answer)
    return question_id


async def get_question_by_id(question_id: int) -> QuestionResponse:
    question = await question_repository.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail=f"Question with id: {question_id} not found")
    optional_answers = await optional_answer_repository.get_by_question_id(question_id)

    optional_answers_data = []
    for i, answer in enumerate(optional_answers):
        optional_answers_data.append({
            f"optional_answer_{i + 1}_id": answer.answer_id,
            f"optional_answer_{i + 1}_text": answer.optional_answer_text
        })

    return QuestionResponse(
        question=question,
        **optional_answers_data[0],
        **optional_answers_data[1],
        **optional_answers_data[2],
        **optional_answers_data[3]
    )


async def update_question(question: QuestionRequest):
    existing_question = await get_question_by_id(question.question.question_id)
    if not existing_question:
        raise HTTPException(
            status_code=404,
            detail=f"Can't update question with id: {question.question.question_id}, question not found"
        )
    else:
        await user_answer_service.delete_user_answer_by_question_id(question.question.question_id)
        await optional_answer_repository.delete_optional_answer_by_question_id(question.question.question_id)
        await question_repository.update_question(question.question)

        optional_answers = [question.option_1, question.option_2, question.option_3, question.option_4]
        for optional_answer in optional_answers:
            optional_answer.question_id = question.question.question_id
            await optional_answer_repository.create_optional_answer(optional_answer)


async def delete_question_by_id(question_id: int):
    existing_question = await get_question_by_id(question_id)
    if not existing_question:
        raise HTTPException(
            status_code=404, detail=f"Can't delete question with id: {question_id}, question not found"
        )
    else:
        await user_answer_service.delete_user_answer_by_question_id(question_id)
        await optional_answer_repository.delete_optional_answer_by_question_id(question_id)
        await question_repository.delete_question_by_id(question_id)

