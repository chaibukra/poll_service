from typing import List
from model.optional_answer import OptionalAnswer
from repository.database import database

TABLE_NAME = "optional_answer"


async def create_optional_answer(optional_answer: OptionalAnswer):
    query = f"""
        INSERT INTO {TABLE_NAME} (question_id, optional_answer_text)
        VALUES (:question_id, :optional_answer_text)
    """
    values = {"question_id": optional_answer.question_id, "optional_answer_text": optional_answer.optional_answer_text}
    await database.execute(query, values)


async def get_by_question_id(question_id: int) -> List[OptionalAnswer]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE question_id=:question_id"
    results = await database.fetch_all(query, values={"question_id": question_id})
    return [OptionalAnswer(**result) for result in results]


async def delete_optional_answer_by_question_id(question_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE question_id=:question_id"
    values = {"question_id": question_id}
    await database.execute(query, values)
