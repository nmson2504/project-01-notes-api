from fastapi import FastAPI

from app.database import init_db

init_db()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Personal Notes API"}
