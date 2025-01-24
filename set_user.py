import os
from dotenv import load_dotenv

# Load existing environment variables (if any)
load_dotenv()


def set_user():
    """Prompt the user for MySQL credentials and update the .env file."""
    # Prompt user for MySQL credentials
    db_user = input("Enter MySQL username: ")
    db_password = input("Enter MySQL password: ")
    db_host = input("Enter MySQL host (default: localhost): ") or "localhost"
    db_name = input(
        "Enter database name (default: javashop_db): ") or "javashop_db"
    secret_key = input(
        "Enter a secret key for the application (leave blank for default): ")

    # Update the .env file with the user inputs
    with open('.env', 'w') as env_file:
        env_file.write(f"DB_USER={db_user}\n")
        env_file.write(f"DB_PASSWORD={db_password}\n")
        env_file.write(f"DB_HOST={db_host}\n")
        env_file.write(f"DB_NAME={db_name}\n")
        env_file.write(f"SECRET_KEY={secret_key or os.urandom(24).hex()}\n")

    print("\nYour .env file has been updated!")


# Run the function to prompt the user
if __name__ == "__main__":
    set_user()
