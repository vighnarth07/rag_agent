import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from server.app.models.document import DocumentChunk

# 1. Initialize the Embedding Model (runs locally)
# We load this once so we don't reload it for every file
print("Loading embedding model... (this may take a moment on first run)")
model = SentenceTransformer('all-MiniLM-L6-v2')

def ingest_pdf(file_path: str, db: Session):
    """
    Parses a PDF, chunks it, embeds it, and saves to DB.
    """
    filename = file_path.split("/")[-1].split("\\")[-1] # Handle both Win/Linux paths
    print(f"Processing file: {filename}")

    # 2. Extract Text with Page Numbers
    doc = fitz.open(file_path)
    text_chunks = []
    
    # We use a recursive splitter to keep sentences together
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            continue
            
        # Split text into chunks
        chunks = splitter.split_text(text)
        
        for chunk_text in chunks:
            text_chunks.append({
                "content": chunk_text,
                "page_number": page_num + 1, # Humans start at page 1
                "source_file": filename
            })

    print(f"Extracted {len(text_chunks)} chunks. Generating embeddings...")

    # 3. Generate Embeddings (Batch processing is faster)
    # We extract just the text content for the model
    contents = [chunk["content"] for chunk in text_chunks]
    embeddings = model.encode(contents)

    # 4. Save to Database
    db_chunks = []
    for i, chunk_data in enumerate(text_chunks):
        db_chunk = DocumentChunk(
            content=chunk_data["content"],
            embedding=embeddings[i].tolist(), # Convert numpy array to list for DB
            source_file=chunk_data["source_file"],
            page_number=chunk_data["page_number"],
            chapter_title="General" # Logic for chapters can be added later
        )
        db_chunks.append(db_chunk)

    db.add_all(db_chunks)
    db.commit()
    print(f"✅ Successfully ingested {len(db_chunks)} chunks from {filename}!")