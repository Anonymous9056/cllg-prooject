from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document
from langchain.llms import Groq
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import settings

class SummarizationService:
    def __init__(self):
        self.llm = Groq(api_key=settings.GROQ_API_KEY)
        self.chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)

    async def summarize_document(self, db: AsyncSession, document_id: int):
        document = await db.get(Document, document_id)
        if not document:
            return None

        chunks = self.text_splitter.split_text(document.content)
        summary = self.chain.run(chunks)
        document.summary = summary
        await db.commit()
        return summary

