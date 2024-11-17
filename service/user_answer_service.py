from fastapi import HTTPException
from api.internalApi.user_service import user_service_api
from model.user_answer import UserAnswer
from repository import user_answer_repository
from service import poll_service


async def create_user_answer(user_answer: UserAnswer):
    user_details = await user_service_api.get_user_by_id(user_answer.user_id)
    if user_details.is_registered:
        user_exist_answers = await user_answer_repository.get_user_answer_count_by_answer_id(user_answer.user_id,
                                                                                             user_answer.answer_id)
        if user_exist_answers >= 1:
            raise HTTPException(status_code=404, detail=f"User already answer this question")

        await user_answer_repository.create_user_answer(user_answer)

    else:
        raise HTTPException(status_code=401, detail=f"User is not registered and not allowed to answer questions")


async def get_question_by_id(question_id: int):
    return await poll_service.get_question_by_id(question_id)


async def delete_user_answer_by_question_id(question_id: int):
    await user_answer_repository.delete_user_answer_by_question_id(question_id)


async def delete_all_user_answers_by_user_id(user_id: int):
    await user_answer_repository.delete_all_user_answers_by_user_id(user_id)


async def update_user_answer(question_id: int, user_answer: UserAnswer):
    user_details = await user_service_api.get_user_by_id(user_answer.user_id)
    if user_details.is_registered:
        user_exist_answers = await user_answer_repository.get_user_answer_count_by_answer_id(user_answer.user_id,
                                                                                             user_answer.answer_id)
        if int(user_exist_answers) >= 1:
            question_id_verify = await user_answer_repository.get_question_id_by_answer_id(user_answer.answer_id)
            if int(question_id) != int(question_id_verify):
                raise HTTPException(status_code=404, detail=f"You can not update this answer for question id"
                                                            f": {question_id} ,this answer belong "
                                                            f"to question id: {question_id_verify}")

            await user_answer_repository.delete_user_answer_by_question_id(question_id)
            await user_answer_repository.create_user_answer(user_answer)

        else:
            raise HTTPException(status_code=404, detail=f"You can not update this answer - User not answer yet "
                                                        f"question id: {question_id}")

    else:
        raise HTTPException(status_code=401, detail=f"User is not registered and not allowed to answer questions")
