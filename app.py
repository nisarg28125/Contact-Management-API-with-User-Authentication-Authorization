from fastapi import FastAPI
from database import create_tables

app = FastAPI()

create_tables()

@app.get("/")

def home():
    return {"message": "Contact Auth API is running!"}