from fastapi import APIRouter, HTTPException
from starlette import status
from model.question_request import QuestionRequest
from model.question_response import QuestionResponse
from service import poll_service

router = APIRouter(
    prefix="/poll",
    tags=["poll"]
)


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question_by_id(question_id: int):
    question = await poll_service.get_question_by_id(question_id)
    return question


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionRequest):
    try:
        question_id = await poll_service.create_question(question)
        return {"message": f"question successfully created - the question id is: {question_id}"}
    except Exception as ex:
        raise HTTPException(
            status_code=404, detail=ex
        )


@router.put("/{question_id}")
async def update_question(question: QuestionRequest):
    await poll_service.update_question(question)
    return {"message": f"question successfully update - the question update details are: {question}"}


@router.delete("/{question_id}")
async def delete_question_by_id(question_id: int):
    await poll_service.delete_question_by_id(question_id)
    return {"message": f"Question: {question_id}, successfully deleted"}


