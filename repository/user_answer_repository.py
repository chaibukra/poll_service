from model.user_answer import UserAnswer
from repository import optional_answer_repository, question_repository
from repository.database import database

TABLE_NAME = "user_answer"


async def create_user_answer(user_answer: UserAnswer):
    query = f"""
        INSERT INTO {TABLE_NAME} (answer_id, user_id)
        VALUES (:answer_id, :user_id)
    """
    values = {"answer_id": user_answer.answer_id, "user_id": user_answer.user_id}
    await database.execute(query, values=values)


async def get_user_answer_count_by_answer_id(user_id: int, answer_id: int) -> int:
    query = f"""
    SELECT COUNT(*) AS answer_count FROM {TABLE_NAME} useranswer
    JOIN {optional_answer_repository.TABLE_NAME} optionalanswer ON useranswer.answer_id = optionalanswer.answer_id 
    WHERE  user_id=:user_id AND optionalanswer.question_id = (SELECT question_id
    FROM {optional_answer_repository.TABLE_NAME}
    WHERE answer_id=:answer_id
    ); """
    count = await database.fetch_one(query, values={"user_id": user_id, "answer_id": answer_id})
    return int(count[0])


async def get_count_for_each_optional_by_question_id(question_id: int):
    query = f"""
        SELECT useranswer.answer_id, optional_answer_text, COUNT(DISTINCT user_id) AS user_count
        FROM {TABLE_NAME} useranswer
        JOIN {optional_answer_repository.TABLE_NAME} optionalanswer 
        ON useranswer.answer_id = optionalanswer.answer_id 
        WHERE useranswer.answer_id IN (
        SELECT answer_id
        FROM {optional_answer_repository.TABLE_NAME}
        WHERE question_id=:question_id
        ) GROUP BY answer_id;
    """

    results = await database.fetch_all(query, values={"question_id": question_id})
    return results


async def get_total_answer_count_by_id_question(question_id: int) -> int:
    query = f"""
        SELECT  COUNT(*) AS answer_count
        FROM {TABLE_NAME}
        WHERE answer_id IN (
        SELECT answer_id
        FROM {optional_answer_repository.TABLE_NAME}
        WHERE question_id=:question_id
        )
    """

    answers_count = await database.fetch_one(query, values={"question_id": question_id})
    return int(answers_count[0])


async def delete_user_answer_by_question_id(question_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME} WHERE answer_id IN(SELECT answer_id
    FROM {optional_answer_repository.TABLE_NAME}
    WHERE question_id=:question_id
    );
    """
    values = {"question_id": question_id}
    await database.execute(query, values=values)


async def get_question_id_by_answer_id(answer_id: int) -> int:
    query = f"""
    SELECT question_id
    FROM {optional_answer_repository.TABLE_NAME}
    WHERE answer_id=:answer_id
    """
    question_id = await database.fetch_one(query, values={"answer_id": answer_id})
    return question_id[0]


async def get_each_answer_by_user_id(user_id: int):
    query = f"""
    SELECT op.question_id , qu.title , op.answer_id, op.optional_answer_text
    FROM {optional_answer_repository.TABLE_NAME} op
    JOIN {question_repository.TABLE_NAME} qu
    ON qu.question_id = op.question_id
    WHERE answer_id IN
    (SELECT answer_id FROM user_answer WHERE user_id=:user_id)
    """
    answers = await database.fetch_all(query, values={"user_id": user_id})
    return answers


async def get_total_answer_count_by_user_id(user_id: int) -> int:
    query = f"""
    SELECT COUNT(*) AS answer_count
        FROM {TABLE_NAME}
        WHERE user_id=:user_id
    """
    answers_count = await database.fetch_one(query, values={"user_id": user_id})
    return int(answers_count[0])


async def delete_all_user_answers_by_user_id(user_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME} 
    WHERE user_id=:user_id
    """
    values = {"user_id": user_id}
    await database.execute(query, values=values)
