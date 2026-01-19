import sys
import os

sys.path.append(os.getcwd())

from server.app.core.database import SessionLocal
from server.app.services.ingestion import ingest_pdf

def main():
    # Directory containing your PDFs
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        print(f"❌ Error: Folder '{data_folder}' not found.")
        print("Please create a 'data' folder and put your 10 PDFs inside it.")
        return

    # Get all PDF files in the directory
    pdf_files = [f for f in os.listdir(data_folder) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"⚠️ No PDF files found in '{data_folder}'.")
        return

    print(f"Found {len(pdf_files)} PDFs. Starting ingestion...")

    db = SessionLocal()
    
    try:
        for filename in pdf_files:
            pdf_path = os.path.join(data_folder, filename)
            print(f"Processing: {filename}...")
            
            try:
                # Call your existing ingestion function
                ingest_pdf(pdf_path, db)
                print(f"✅ Successfully ingested: {filename}")
            except Exception as e:
                print(f"❌ Failed to ingest {filename}: {e}")
                
    finally:
        db.close()
        print("All done!")

if __name__ == "__main__":
    main()