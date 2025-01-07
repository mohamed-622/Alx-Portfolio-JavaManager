from app import create_app

# Create the Flask app instance using the create_app function
app = create_app()

# Start the Flask development server when run.py is executed
if __name__ == "__main__":
    app.run(debug=True)
