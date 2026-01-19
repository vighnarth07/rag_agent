import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Construct the Database URL
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# 3. Create the SQLAlchemy Engine
# This represents the core interface to the database
engine = create_engine(DATABASE_URL)

# 4. Create a SessionLocal class
# Each request will create a new session instance from this class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base class for our database models
Base = declarative_base()

# 6. Dependency for FastAPI
# This function allows API endpoints to get a DB session and closes it automatically after request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()