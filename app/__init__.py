from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Load configuration from the 'Config' class in config.py
    app.config.from_object('config.Config')

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        # Import and register routes
        from . import routes
        
        # Create the tables in the database (skip migrations for now)
        db.create_all()

        # Return the app instance
        return app
