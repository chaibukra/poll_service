from typing import Optional
from model.question import Question
from repository.database import database

TABLE_NAME = "question"


async def create_question(question: Question) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (title)
        VALUES(:title)
    """
    values = {"title": question.title}

    async with database.transaction():
        await database.execute(query, values=values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]


async def get_question_by_id(question_id: int) -> Optional[Question]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE question_id=:question_id"
    result = await database.fetch_one(query, values={"question_id": question_id})
    if result:
        return Question(**result)
    else:
        return None


async def update_question(question: Question):
    query = f"""
        UPDATE {TABLE_NAME}
        SET title = :title
        WHERE question_id=:question_id
    """
    values = {"title": question.title, "question_id": question.question_id}
    await database.execute(query, values=values)


async def delete_question_by_id(question_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE question_id=:question_id"
    await database.execute(query, values={"question_id": question_id})


async def get_total_question_count() -> int:
    query = f"SELECT COUNT(*) AS question_count FROM {TABLE_NAME}"
    result = await database.fetch_one(query)
    return result[0]

