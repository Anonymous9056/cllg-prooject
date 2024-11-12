# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from sqlalchemy.ext.asyncio import AsyncSession
# from db.postgres import get_db
# from app.services.document_service import document_service
# from app.services.summarization_service import summarization_service
# from pydantic import BaseModel

# router = APIRouter()

# class DocumentResponse(BaseModel):
#     id: int
#     filename: str
#     content_type: str
#     summary: str | None

# @router.post("/", response_model=DocumentResponse)
# async def create_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
#     try:
#         return await document_service.create_document(db, file)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/{document_id}", response_model=DocumentResponse)
# async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
#     document = await document_service.get_document(db, document_id)
#     if document is None:
#         raise HTTPException(status_code=404, detail="Document not found")
#     return document

# @router.get("/user/{user_id}", response_model=List[int])
# async def get_document_ids_for_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     documents = await document_service.get_all_documents(db, user_id=user_id)
#     return [document.id for document in documents]