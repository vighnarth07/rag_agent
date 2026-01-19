from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from server.app.core.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    
    # The actual text content used for RAG
    content = Column(Text, nullable=False)
    
    # 384 dimensions matches the 'all-MiniLM-L6-v2' model we will use
    embedding = Column(Vector(384))
    
    # Metadata for strict citation
    source_file = Column(String, nullable=False)   # e.g. "Physics_Vol1.pdf"
    chapter_title = Column(String, nullable=True)  # e.g. "Chapter 1"
    page_number = Column(Integer, nullable=False)  # e.g. 42
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())