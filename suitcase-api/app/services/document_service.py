from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.models.document import Document
from app.utils.file_processor import process_file
from db.qdrant import get_qdrant_client
from qdrant_client.models import PointStruct
from langchain.embeddings import HuggingFaceEmbeddings

class DocumentService:
    def __init__(self):
        # self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.qdrant_client = get_qdrant_client()

    async def create_document(self, db: AsyncSession, file: UploadFile):
        content = process_file(file)
        if content is None:
            raise ValueError("Unsupported file type")

        new_document = Document(
            filename=file.filename,
            content_type=file.content_type,
            content=content,
            file_data=await file.read()
        )
        db.add(new_document)
        await db.commit()
        await db.refresh(new_document)

        # Create embedding and store in Qdrant
        # embedding = self.embeddings.embed_query(content)
        # self.qdrant_client.upsert(
        #     collection_name="documents",
        #     points=[PointStruct(id=new_document.id, vector=embedding, payload={"content": content})]
        # )

        return new_document

    async def get_document(self, db: AsyncSession, document_id: int):
        return await db.get(Document, document_id)

    async def get_all_documents(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        query = db.query(Document).offset(skip).limit(limit)
        return await query.all()

document_service = DocumentService()