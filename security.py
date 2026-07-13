from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

def create_access_token(data: dict):
    copied_data = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=30)

    copied_data.update({"exp": expire_time})

    token = jwt.encode(copied_data, SECRET_KEY, algorithm=ALGORITHM)


    return token

