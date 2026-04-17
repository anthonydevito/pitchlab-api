from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Using SQLite for this project (creates a local file) 
# Normally, we'd point this URL to a PostgreSQL instance.
SQLALCHEMY_DATABASE_URL = "sqlite:///./pitchlab.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Start DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
