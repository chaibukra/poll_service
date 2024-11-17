from fastapi import HTTPException
from repository import user_answer_repository, question_repository, optional_answer_repository


async def get_count_of_each_optional_answer_by_id(question_id: int):
    result = await user_answer_repository.get_count_for_each_optional_by_question_id(question_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"There is not question with id {question_id} or no one has "
                                                    f"answer to this question")
    else:
        return result


async def get_total_answer_count_by_id_question(question_id: int) -> int:
    answers_count = await user_answer_repository.get_total_answer_count_by_id_question(question_id)
    if not answers_count:
        raise HTTPException(status_code=404, detail=f"There is not question with id {question_id} or no one has "
                                                    f"answer to this question")
    else:
        return answers_count


async def get_each_answer_by_user_id(user_id: int):
    answers = await user_answer_repository.get_each_answer_by_user_id(user_id)
    if not answers:
        raise HTTPException(status_code=404, detail=f"The user with id {user_id} has "
                                                    f"not answer to any question")
    else:
        return answers


async def get_total_answer_count_by_user_id(user_id: int) -> int:
    answers_count = await user_answer_repository.get_total_answer_count_by_user_id(user_id)
    if not answers_count:
        raise HTTPException(status_code=404, detail=f"The user with id {user_id} has not answered "
                                                    f"any question")
    else:
        return answers_count


async def get_all():
    all_questions_data = []
    number_of_total_question = await question_repository.get_total_question_count()

    for question_id in range(number_of_total_question):
        question_id += 1
        question_details = await question_repository.get_question_by_id(question_id)
        optional_answers = await optional_answer_repository.get_by_question_id(question_id)
        answers_count = await user_answer_repository.get_count_for_each_optional_by_question_id(question_id)

        question_data = {f"question_{question_id}": question_details}
        for i, answer in enumerate(optional_answers):
            user_count = 0
            for count_answer in answers_count:
                if count_answer.answer_id == answer.answer_id:
                    user_count = count_answer.user_count
                    break

            question_data[f"optional_answer_{i + 1}_id"] = answer.answer_id
            question_data[f"optional_answer_{i + 1}_text"] = answer.optional_answer_text
            question_data[f"user_count_for_answer_{i + 1}"] = user_count

        all_questions_data.append(question_data)

    return all_questions_data
