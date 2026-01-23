# Ticketsystem

## Project Description

This project is a simple ticket system developed as a school project. The assignment was to build a lightweight helpdesk solution for a fictional company called TechSupport AS, which was struggling to keep track of daily support requests.

The solution is built with Flask and uses a MariaDB database with two tables: users and tickets. Employees can register, log in, and use the system based on their role:

- Regular users can create tickets and view the status of their own cases.
- Tech support workers can see all tickets, assign themselves cases, and update the status (open / in progress / closed).

## How to Run the Project

### 1. Install Dependencies

After opening the project folder in your code editor, install the required Python dependencies.

It is recommended (but optional) to use a virtual environment so you don’t clutter your global Python installation.

Example:

    python -m venv venv
    source venv/bin/activate        # macOS/Linux
    venv\Scripts\activate           # Windows

Then install the dependencies:

    pip install -r requirements.txt

If you don’t have the `requirements.txt`, install manually:

    pip install flask mysql-connector-python

---

## Database Setup (MariaDB / MySQL)

To run the webpage, you must use a MySQL-based database (such as MariaDB).

1. Create a new database in MariaDB/MySQL.  
2. Fill out your database connection settings inside **app.py**:

Find this inside [`app.py`](/app.py):

    def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST or "localhost",
        user=DB_USER or "your_user_name",
        password=DB_PASSWORD or "your_password",
        database=DB_KANTINE or "your_database_name"
    )

Make sure these match your local database configuration.

---

## Running the Project

After installing dependencies and configuring the database, you can start the server with:

    python app.py

Then open your browser and visit:

    http://127.0.0.1:5000/
