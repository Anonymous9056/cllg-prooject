from langchain_groq import ChatGroq
from langchain.chains import ConversationChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from fastapi import WebSocket
from typing import List, AsyncGenerator
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from models.chat import ChatResponse
import json
import os
from dotenv import load_dotenv

load_dotenv()

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

store = {}

prompt = ChatPromptTemplate.from_messages([
    ("system", """You're an assistant for lawyers who will assist with summarization, legal research, and drafting documents.  The affidavit should:
  1. Be properly formatted for court submission
  2. Include all standard legal phrases and formatting
  3. Number all paragraphs
  4. Include proper spacing and alignment
  5. Be ready for direct copy-paste into Microsoft Word

  Format the output with proper line breaks using \n and proper spacing.
  Use ONLY plain text formatting that will work in any text editor."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.7,
    max_retries=1,
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=True  # Enable streaming
)

def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]

class ChatService:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=0.7,
            max_retries=1,
            api_key=os.getenv("GROQ_API_KEY"),
            streaming=True  # Enable streaming
        )
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)
        self.qa_chain = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="question",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for the user.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="conversation_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                    default="",
                    is_shared=True,
                ),
            ]
        )

    async def stream_chat(self, websocket: WebSocket, user_id: str, conversation_id: str):
        await websocket.accept()
        
        try:
            while True:
                data = await websocket.receive_text()
                query = json.loads(data)["question"]
                
                # Get the streaming response
                # response_stream = await self.qa_chain.astream(
                #     {"question": query},
                #     config={'configurable': {"user_id": user_id, "conversation_id": conversation_id}}
                # )
                
                # print(response_stream)
                
                async for chunk in self.qa_chain.astream(
                    {"question": query},
                    config={'configurable': {"user_id": user_id, "conversation_id": conversation_id}}
                ):
                    if hasattr(chunk, 'content'):
                        await websocket.send_text(json.dumps({
                            "type": "chunk",
                            "content": chunk.content
                        }))
                
                # Send end message
                await websocket.send_text(json.dumps({
                    "type": "end",
                    "content": ""
                }))
                
        except Exception as e:
            print(e)
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": str(e)
            }))
        finally:
            await websocket.close()

    async def chat(self, query: str, user_id: str = "123", conversation_id: str = "1"):
        response = await self.qa_chain.ainvoke(
            {"question": query},
            config={'configurable': {"user_id": user_id, "conversation_id": conversation_id}}
        )
        return ChatResponse(type="model", content=response.content)

# Needs to work for mltiple users later on.
chat_service = ChatService()