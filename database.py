import sqlite3


DATABASE_NAME = "contacts.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            username TEXT unique NOT NULL,
            email TEXT unique NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT
        )
    ''')


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts(

            contact_id TEXT PRIMARY KEY,

            first_name TEXT NOT NULL,

            last_name TEXT,

            phone TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            company TEXT NOT NULL,

            job_title TEXT,

            city TEXT NOT NULL,

            created_at TEXT

        )
        """
    )



    connection.commit()
    connection.close()