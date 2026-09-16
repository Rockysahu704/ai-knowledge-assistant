from fastapi import APIRouter

from  schemas.ask import AskQuery, AskResponse
from services import ask_service





router = APIRouter()


@router.post("/api/ask/", response_model=AskResponse)
async def ask_question(user_query:AskQuery):

    response = ask_service.ask_question(user_query)
    return response


