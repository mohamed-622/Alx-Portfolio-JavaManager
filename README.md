# ALX-portfolio-JavaManager
A coffee shop management system designed to streamline operations, enhance customer service, and optimize workflow, built as part of the ALX portfolio project.


# Flask App Setup Guide

### 1. **MySQL Server Installation**
   - **Install MySQL Server**: Ensure MySQL server is installed and running on your machine (or remote server).
   - **Check MySQL Status**: Confirm MySQL is running, and you can connect via command-line or a MySQL client.

   To install MySQL:
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get update
     sudo apt-get install mysql-server
     ```
   - **Windows**: Download MySQL Installer from [MySQL Downloads](https://dev.mysql.com/downloads/installer/).
  

### 2. **Create MySQL User**
   - **Create a MySQL user** with the necessary permissions. 

   You can create any MySQL user you prefer. To create a user named `javashop`, log into MySQL:
   ```bash
   sudo mysql -u root -p
   ```

   Then, create the user and grant privileges:
   ```sql
   CREATE USER 'javashop'@'localhost' IDENTIFIED BY '1020';
   GRANT ALL PRIVILEGES ON *.* TO 'javashop'@'localhost';
   FLUSH PRIVILEGES;
   ```

   Alternatively, you can create a different user if you prefer.

### 3. **Clone the Repository**
   - Clone this repository to your local machine:
     ```bash
     git clone https://github.com/mohamed-622/Alx-Portfolio-JavaManager.git
     cd Alx-Portfolio-JavaManager
     ```
### 4. **Set Up Virtual Environment**
   - Create and activate a virtual environment to isolate the project dependencies:
     - **For Windows**:
       ```bash
       python -m venv venv
       venv\Scripts\activate
       ```
     - **For macOS/Linux**:
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```

   - Once activated, the terminal prompt should change to indicate the virtual environment is active (e.g., `(venv)`).

### 5. **Install Dependencies**
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

### 6. **Set Up Environment Variables**

   - Run the `set_user.py` script to set up your database credentials:
     ```bash
     python set_user.py
     ```

     The script will prompt you to enter the following information:
     - **MySQL username**: Enter the MySQL username(e.g., `javashop` or a different one you created).
     - **MySQL password**: Enter the password for the MySQL user you've created.
     - **MySQL host**: Enter the host (default is `localhost`).
     - **Database name**: Enter the name of the database (default is `javashop_db`).
     - **Secret key**: Optionally enter a secret key for the application (if left blank, a random key will be generated).

     This script will automatically update the `.env` file with the provided details.

### 7. **Run the Application**
   ```bash
   python run.py
   ```

### 8. **Access the Application**
   - Open your browser and go to [http://localhost:5000](http://localhost:5000).

### 9. **Troubleshooting**
   - Ensure that MySQL is running and that the credentials in the `.env` file are correct.
   - If the app can't connect to the database, double-check that the user has the necessary permissions and the correct database is specified.
