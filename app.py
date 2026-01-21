from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Read environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TechSupportAS = os.getenv("DB_TechSupportAS")
SECRET_KEY = os.getenv("SECRET_KEY") or "supersecretkey"

app.secret_key = SECRET_KEY

# ----- Fill out your database connection settings ----- #

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host = DB_HOST or "localhost",
        user = DB_USER or "your_user_name",
        password = DB_PASSWORD or "your_password",
        database = DB_TechSupportAS or "your_database_name"
    )

# Create tables
def users_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100),
                username VARCHAR(50) NOT NULL UNIQUE,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL,
                bruker_role BOOLEAN DEFAULT TRUE,
                drift_role BOOLEAN DEFAULT FALSE
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

users_table()

def tickets_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'åpen',
                process_id INT
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

tickets_table()

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        db_user = cursor.fetchone()
        cursor.close()
        connection.close()

        roles = []
        if db_user:
            if db_user['bruker_role']:
                roles.append('bruker')
            if db_user['drift_role']:
                roles.append('drift')
        
        session['username'] = username
        session['roles'] = roles

        if roles == ['bruker']:
            session['active_role'] = 'bruker'
            return redirect(url_for('main_menu'))
        return redirect(url_for('chose_role'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND username = %s", (email, username))
        existing_db_user = cursor.fetchone()
        cursor.close()
        connection.close()

        if existing_db_user:
            return render_template('login.html', error="E-post eller brukernavn er allerede registrert")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (email, username, first_name, last_name, password, bruker_role, drift_role) VALUES (%s, %s, %s, %s, %s, TRUE, FALSE)", (email, username, first_name, last_name, password))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/chose_role', methods=['GET', 'POST'])
def chose_role():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    roles = session.get("roles", [])
    if request.method == "POST":
        selected_role = request.form.get("role")
        if selected_role in roles:
            session["active_role"] = selected_role
            return redirect(url_for("main_menu"))
        else:
            return render_template("role.html", roles=roles, error="Ugyldig rolle valgt.")
    
    return render_template("role.html", roles=roles)

@app.route('/')
def main_menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    role = session.get('active_role')

    return render_template('main_menu.html', role=role)

if __name__ == '__main__':
    app.run(debug=True)