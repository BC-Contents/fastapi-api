import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE:str = os.getenv("APP_TITLE","Library")
APP_VERSION:str = os.getenv("APP_VERSION","0.0.1")
APP_DESCRIPTION:str = os.getenv(
    "APP_DESCRIPTION",
    "app de una librería"
)

DATABASE_NAME: str = os.getenv("DATABASE_NAME","db.sqlite3")
DATABASE_URL:str = os.getenv("DATABASE_URL","sqlite:///./db.sqlite3")