from fastapi import UploadFile
from sqlalchemy.orm import Session
from langchain_community.document_loaders import PyPDFLoader
from app.models.Document import Document
from sentence_transformers import SentenceTransformer
import tempfile

class DocsService:

    @classmethod
    def process(cls, db: Session, file: UploadFile):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.file.read())
                path = tmp.name

            loader = PyPDFLoader(path)

            pages = loader.load()

            content = "".join([page.page_content for page in pages])

            model = SentenceTransformer('BAAI/bge-small-en')
            vector = model.encode(content)

            meta = pages[0].metadata if pages else {}
            
            document = Document(
                filename=file.filename, 
                content=content, 
                embedding=vector,   
                meta=meta
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            return {"document_id": document.id, "filename": document.filename}

        except Exception as e:
            print(f"Error processing document: {e}")
            raise e

