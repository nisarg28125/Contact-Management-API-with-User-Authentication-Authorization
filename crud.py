from database import get_connection
from security import hash_password
from datetime import datetime
import uuid

def create_user(user):
    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(user.password)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_id = "U" + str(uuid.uuid4())[:8]

    cursor.execute(
        """
        INSERT INTO users (user_id, full_name, username, email, password_hash, role, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            user.full_name,
            user.username,
            user.email,
            password_hash,
            user.role,
            True,
            created_at
        )

    )

    connection.commit()
    connection.close()

    return user_id

def get_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return dict(user)
    else:
        return None