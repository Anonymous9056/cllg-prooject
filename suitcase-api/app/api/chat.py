from fastapi import APIRouter, WebSocket, Depends
from services.chat_service import chat_service
from models.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.websocket("/ws/{user_id}/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, conversation_id: str):
    await chat_service.stream_chat(websocket, user_id, conversation_id)

@router.post("/", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    return await chat_service.chat(chat_request.query)