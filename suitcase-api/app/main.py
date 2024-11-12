from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from api import chat, document, health
from core import supertokens_config
from core.config import settings
# from app.db.postgres import init_db
# from app.db.qdrant import init_qdrant


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, debug=True)

if settings.SUPERTOKENS_CONNECTION_URI is not None:
    supertokens_config.init_supertokens()
    app.add_middleware(get_middleware())
    print("Supertokens set up")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"]
)

# app.include_router(document.router, prefix="/documents", tags=["documents"])
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

# @app.on_event("startup")
# async def startup():
#     await init_db()
#     await init_qdrant()


@app.get("/")
async def root():
    return {"message": "Suitcase"}