
from fastapi import FastAPI

from app.database import init_db
from app.routers.notes import router # import app.routers.notes để include_router bên dưới

init_db()

app = FastAPI()

app.include_router(router) # đưa các routes được khai báo trong routers/notes.py vào FastAPI app này
'''
Nguyên tắc & Lời khuyên về kiến trúc
Khi nào nên khai báo route trực tiếp trong main.py?
Các route toàn cục không thuộc về một nhóm chức năng cụ thể nào, ví dụ: @app.get("/health"), @app.get("/metrics"), @app.get("/version").

Khi nào nên chia ra file router riêng (như notes.py)?
Khi route thuộc về một nhóm tài nguyên/đối tượng cụ thể (như users, notes, products, auth).

Việc gom các route liên quan vào file riêng giúp mã nguồn gọn gàng, dễ bảo trì và mở rộng khi dự án lớn lên.
'''

@app.get("/")
def root():
    return {"message": "Personal Notes API"}