import io
from typing import Union
from fastapi import UploadFile
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

def process_file(file: UploadFile) -> Union[str, None]:
    content = file.file.read()
    
    if file.content_type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(content))
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(io.BytesIO(content))
    elif file.content_type == "text/plain":
        return content.decode("utf-8")
    else:
        return None

def extract_text_from_pdf(file_stream: io.BytesIO) -> str:
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_stream: io.BytesIO) -> str:
    doc = DocxDocument(file_stream)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])