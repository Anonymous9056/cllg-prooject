from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    user_id: str = "123"
    conversation_id: str = "1"

class ChatResponse(BaseModel):
    type: str
    content: str