import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize the SQLAlchemy instance
db = SQLAlchemy()


def create_database_if_not_exists(uri):
    """Check if the database exists, and create it if it doesn't."""
    # Parse the URI for connection parameters
    connection = pymysql.connect(
        host="localhost",
        user="javashop",
        password="1002",
    )

    db_name = "javashop_db"

    # Check if the database exists
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
        result = cursor.fetchone()

        if not result:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
    connection.close()


def create_app():
    """Create the Flask app instance."""
    # Ensure the database exists
    create_database_if_not_exists(Config.SQLALCHEMY_DATABASE_URI)

    # Create the app
    app = Flask(__name__)

    # Load configuration from the 'Config' class in config.py
    app.config.from_object('config.Config')

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        # Import and register routes
        from . import routes

        # Create the tables in the database
        db.create_all()

        # Return the app instance
        return app
