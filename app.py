from fastapi import FastAPI
from database import create_tables
from routers import auth, users



app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

create_tables()

@app.get("/")

def home():
    return {"message": "Contact Auth API is running!"}