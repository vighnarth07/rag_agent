import uvicorn
import os
import sys

# Fix imports: Add the project root directory to sys.path
# This allows 'server.app...' imports to work regardless of where you run the script from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.app.api.routes import router

app = FastAPI(title="RAG Chatbot API")

# Configure CORS (Cross-Origin Resource Sharing)
# This allows a frontend running on a different port to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes defined in routes.py
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    # Use the app object directly when running via python command
    print("🚀 Starting Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Note: 'reload=True' works best when running via 'uvicorn server.main:app --reload'