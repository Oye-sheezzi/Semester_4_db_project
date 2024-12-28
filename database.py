import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="simulation_bank_db"
    )

def create_user(username, email, phone_number, balance, password):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, phone_number, balance, password) VALUES (%s, %s, %s, %s, %s)",
        (username, email, phone_number, balance, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user(username):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_balance(user_id, amount):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def record_transaction(user_id, amount, transaction_type, description):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, transaction_type, description) VALUES (%s, %s, %s, %s)",
        (user_id, amount, transaction_type, description)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_transaction_history(user_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions

def get_balance(user_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()
    cursor.close()
    conn.close()
    return balance[0]
