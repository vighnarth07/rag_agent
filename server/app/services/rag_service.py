import os
from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import select
from server.app.models.document import DocumentChunk
from sentence_transformers import SentenceTransformer

# Initialize Clients
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def query_rag(user_question: str, db: Session):
    """
    Retrieves context and generates an answer using Groq.
    Returns: (answer_text, source_list)
    """
    # 1. Convert Question to Vector
    print(f"Generating embedding for: '{user_question}'...")
    query_embedding = embedding_model.encode(user_question).tolist()

    # 2. Search Database
    print("Searching database for relevant context...")
    stmt = select(DocumentChunk).order_by(
        DocumentChunk.embedding.cosine_distance(query_embedding)
    ).limit(5)
    
    results = db.execute(stmt).scalars().all()
    
    # Handle no results
    if not results:
        return "I could not find any relevant information.", []

    # 3. Prepare Context
    context_str = ""
    for doc in results:
        source_id = f"{doc.source_file} (Page {doc.page_number})"
        context_str += f"Source: {source_id}\nContent: {doc.content}\n\n"

    print(f"Found {len(results)} relevant chunks. Sending to Groq LLM...")

    # 4. Construct Prompt
    system_prompt = """
    You are an intelligent academic assistant. 
    Answer the user's question strictly based on the provided Context. 
    If the answer is not in the context, say "Please ask a question that is related to the uploaded documents.".
    """

    user_prompt = f"Context:\n{context_str}\n\nQuestion:\n{user_question}"

    # 5. Call Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="openai/gpt-oss-120b",
        temperature=0.1,
    )
    
    answer_text = chat_completion.choices[0].message.content

    # 6. Format Sources for the API
    formatted_sources = []
    for doc in results:
        formatted_sources.append({
            "source_file": doc.source_file,
            "page_number": doc.page_number,
            "content": doc.content
        })

    return answer_text, formatted_sources