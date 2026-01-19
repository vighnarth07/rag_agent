import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from server.app.core.database import get_db
from server.app.services.ingestion import ingest_pdf
from server.app.services.rag_service import query_rag
from server.app.schemas.payloads import ChatRequest, ChatResponse, IngestResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Unpack the tuple (answer, sources)
        answer_text, sources_list = query_rag(request.question, db)
        
        return ChatResponse(
            answer=answer_text, 
            sources=sources_list
        )
    except Exception as e:
        print(f"Error in chat_endpoint: {e}") # Print error to terminal
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    temp_folder = "temp_uploads"
    os.makedirs(temp_folder, exist_ok=True)
    file_path = os.path.join(temp_folder, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        ingest_pdf(file_path, db)
        
        return IngestResponse(
            filename=file.filename,
            chunks_added=0,
            status="Success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)