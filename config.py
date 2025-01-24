import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # MySQL database connection URI
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default to random secret key if not provided
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
