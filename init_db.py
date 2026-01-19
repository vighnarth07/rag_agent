import sys
import os

# Fix path
sys.path.append(os.getcwd())

from server.app.core.database import engine, Base
# Import the model so SQLAlchemy knows it exists before creating tables
from server.app.models.document import DocumentChunk

def init_db():
    print("Creating database tables...")
    try:
        # This checks the database and creates any missing tables defined in 'Base'
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    init_db()