from pydantic import BaseModel

class Document(BaseModel):
    filename: str
    content: str
    meta: dict
    embedding: list[float]