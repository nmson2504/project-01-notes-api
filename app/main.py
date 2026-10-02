
from fastapi import FastAPI

from app.database import init_db
from app.routers.notes import router # import app.routers.notes để include_router bên dưới

init_db()

app = FastAPI()

app.include_router(router) # đưa các routes được khai báo trong routers/notes.py vào FastAPI app này


@app.get("/")
def root():
    return {"message": "Personal Notes API"}