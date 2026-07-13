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
    


def create_contact(contact):

    connection = get_connection()

    cursor = connection.cursor()


    contact_id = "C" + str(uuid.uuid4())[:8]


    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO contacts
        (
            contact_id,
            first_name,
            last_name,
            phone,
            email,
            company,
            job_title,
            city,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            contact_id,
            contact.first_name,
            contact.last_name,
            contact.phone,
            contact.email,
            contact.company,
            contact.job_title,
            contact.city,
            created_at
        )

    )


    connection.commit()

    connection.close()


    return contact_id


def get_all_contacts():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM contacts
        """
    )


    contacts = cursor.fetchall()


    connection.close()


    return [
        dict(contact)
        for contact in contacts
    ]


def get_contact_by_id(contact_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM contacts
        WHERE contact_id = ?
        """,
        (contact_id,)
    )


    contact = cursor.fetchone()


    connection.close()


    if contact:

        return dict(contact)


    return None



def update_contact(contact_id, contact):

    connection = get_connection()

    cursor = connection.cursor()


    update_fields = []

    values = []


    for field, value in contact.model_dump(exclude_unset=True).items():

        update_fields.append(f"{field} = ?")

        values.append(value)


    if not update_fields:

        connection.close()

        return False


    values.append(contact_id)


    query = f"""
    UPDATE contacts
    SET {", ".join(update_fields)}
    WHERE contact_id = ?
    """


    cursor.execute(query, values)


    connection.commit()


    updated = cursor.rowcount


    connection.close()


    return updated > 0


def delete_contact(contact_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE
        FROM contacts
        WHERE contact_id = ?
        """,
        (contact_id,)
    )


    connection.commit()


    deleted = cursor.rowcount


    connection.close()


    return deleted > 0


def search_contacts(name=None, company=None, city=None):

    connection = get_connection()

    cursor = connection.cursor()


    query = """
    SELECT *
    FROM contacts
    WHERE 1=1
    """

    values = []


    if name:

        query += """
        AND (
            first_name LIKE ?
            OR last_name LIKE ?
        )
        """

        values.extend(
            [
                f"%{name}%",
                f"%{name}%"
            ]
        )


    if company:

        query += """
        AND company LIKE ?
        """

        values.append(
            f"%{company}%"
        )


    if city:

        query += """
        AND city LIKE ?
        """

        values.append(
            f"%{city}%"
        )


    cursor.execute(
        query,
        values
    )


    contacts = cursor.fetchall()


    connection.close()


    return [
        dict(contact)
        for contact in contacts
    ]



def sort_contacts(sort_by="first_name", order="asc"):

    connection = get_connection()

    cursor = connection.cursor()


    allowed_columns = [
        "first_name",
        "last_name",
        "company",
        "city",
        "created_at"
    ]


    if sort_by not in allowed_columns:

        sort_by = "first_name"


    if order.lower() not in ["asc", "desc"]:

        order = "asc"


    query = f"""
    SELECT *
    FROM contacts
    ORDER BY {sort_by} {order.upper()}
    """


    cursor.execute(query)


    contacts = cursor.fetchall()


    connection.close()


    return [
        dict(contact)
        for contact in contacts
    ]



def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM contacts
        """
    )

    total_contacts = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(DISTINCT company)
        FROM contacts
        """
    )

    total_companies = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(DISTINCT city)
        FROM contacts
        """
    )

    total_cities = cursor.fetchone()[0]


    connection.close()


    return {
        "total_contacts": total_contacts,
        "total_companies": total_companies,
        "total_cities": total_cities
    }


def get_all_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            full_name,
            username,
            email,
            role,
            is_active,
            created_at
        FROM users
        """
    )

    users = cursor.fetchall()

    connection.close()

    return [
        dict(user)
        for user in users
    ]

def change_password(user_id, password_hash):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE user_id = ?
        """,
        (
            password_hash,
            user_id
        )
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated > 0

def disable_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = 0
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated > 0


def enable_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_active = 1
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated > 0

def delete_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted > 0