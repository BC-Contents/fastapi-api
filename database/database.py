from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from config.config_variables import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Generator[Session,None,None]:
    db: Session = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

