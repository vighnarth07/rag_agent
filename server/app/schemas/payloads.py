from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str

# New model for a single source citation
class SourceModel(BaseModel):
    source_file: str
    page_number: int
    content: str

# Updated response to include the list of sources
class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceModel] # <--- Added this

class IngestResponse(BaseModel):
    filename: str
    chunks_added: int
    status: str