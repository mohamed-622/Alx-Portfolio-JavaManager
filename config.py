import os

class Config:
    # MySQL database connection URI
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://javashop:1002@localhost/javashop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Secret key for session management
