from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db

# Create the Flask app instance using the create_app function
app = create_app()

@app.cli.command("reset_db")
def reset_db():
    """Drop all tables and recreate them."""
    with app.app_context():
        db.drop_all()  # Drops all tables
        db.create_all()  # Recreates all tables
        print("Database has been reset successfully.")

# Start the Flask development server when run.py is executed
if __name__ == "__main__":
    app.run(debug=True)