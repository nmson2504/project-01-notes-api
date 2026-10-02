from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import NoteModel
from app.schemas import Note, NoteCreate

router = APIRouter()


def get_note_or_404(note_id: int, db: Session) -> NoteModel:
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note


@router.get("/notes", response_model=list[Note])
def list_notes(db: Session = Depends(get_db)):
    return db.scalars(select(NoteModel)).all()


@router.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    return get_note_or_404(note_id, db)


@router.post("/notes", status_code=201, response_model=Note)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = NoteModel(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    payload: NoteCreate,
    db: Session = Depends(get_db),
):
    note = get_note_or_404(note_id, db)
    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note


@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_or_404(note_id, db)
    db.delete(note)
    db.commit()
    return Response(status_code=204)



"""
DDịnh nghĩa các API Endpoints (Router) quản lý ghi chú (Notes) trong ứng dụng FastAPI. Đây là nơi kết nối giữa HTTP Requests từ client với logic thao tác Database (CRUD) thông qua SQLAlchemy và Pydantic.

Dưới đây là giải thích chi tiết chức năng và nhiệm vụ của từng phần:

1. Khai báo APIRouter & Imports

router = APIRouter()
APIRouter(): Dùng để nhóm các đường dẫn API liên quan lại với nhau (trong trường hợp này là quản lý notes). Việc dùng Router giúp chia nhỏ ứng dụng thành nhiều module dễ quản lý thay vì viết tất cả các endpoint vào file main.py.

2. Hàm bổ trợ get_note_or_404 (Helper Function)

def get_note_or_404(note_id: int, db: Session) -> NoteModel:
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note
Nhiệm vụ: Tìm kiếm ghi chú theo note_id.

Cơ chế:

Sử dụng db.get(NoteModel, note_id) (cú pháp chuẩn SQLAlchemy 2.0 để tìm theo Khóa chính).

Nếu không tìm thấy (None), lập tức ném ra lỗi HTTPException(status_code=404) báo cho client.

Nếu tìm thấy, trả về đối tượng NoteModel.

Mục đích: Tái sử dụng code, giúp các hàm read_note, update_note, và delete_note không bị trùng lặp đoạn logic kiểm tra tồn tại.

3. Chi tiết 5 API Endpoints (CRUD)1. GET /notes – Lấy danh sách tất cả ghi chú (Read All)Python@router.get("/notes", response_model=list[Note])
def list_notes(db: Session = Depends(get_db)):
    return db.scalars(select(NoteModel)).all()
Chức năng: Truy vấn toàn bộ ghi chú có trong Database.Cơ chế:Depends(get_db): Tự động mượn một Session kết nối DB từ database.py.db.scalars(select(NoteModel)).all(): Thực hiện câu lệnh SQL SELECT * FROM notes và trả về danh sách đối tượng NoteModel.response_model=list[Note]: FastAPI tự động chuyển đổi danh sách các NoteModel này thành danh sách các Pydantic Schema Note dạng JSON.2. GET /notes/{note_id} – Lấy chi tiết 1 ghi chú (Read One)Python@router.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    return get_note_or_404(note_id, db)
Chức năng: Trả về thông tin của ghi chú theo note_id.Cơ chế: Gọi hàm get_note_or_404(). Nếu có sẽ trả về dữ liệu (mã HTTP 200 OK), nếu không có sẽ trả về lỗi 404 Not Found.3. POST /notes – Tạo ghi chú mới (Create)Python@router.post("/notes", status_code=201, response_model=Note)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = NoteModel(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
Chức năng: Tạo một bản ghi mới trong Database.Cơ chế:payload: NoteCreate: Nhận JSON từ client và kiểm tra hợp lệ bằng Pydantic.NoteModel(...): Tạo object ORM mới từ payload.db.add(note): Đưa bản ghi vào trạng thái chờ lưu (pending).db.commit(): Thực thi câu lệnh INSERT INTO xuống Database.db.refresh(note): Tải lại dữ liệu từ DB lên object note để lấy id vừa được DB tự động sinh ra.Trả về note cùng trạng thái HTTP 201 Created.4. PUT /notes/{note_id} – Cập nhật ghi chú (Update)Python@router.put("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    payload: NoteCreate,
    db: Session = Depends(get_db),
):
    note = get_note_or_404(note_id, db)
    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note
Chức năng: Thay đổi tiêu đề (title) và nội dung (content) của một ghi chú có sẵn.Cơ chế: Tìm ghi chú qua get_note_or_404() $\rightarrow$ Gán lại giá trị mới cho các thuộc tính $\rightarrow$ db.commit() để lưu câu lệnh UPDATE xuống DB.5. DELETE /notes/{note_id} – Xóa ghi chú (Delete)Python@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_or_404(note_id, db)
    db.delete(note)
    db.commit()
    return Response(status_code=204)
Chức năng: Xóa bỏ ghi chú khỏi Database.Cơ chế:Tìm ghi chú qua get_note_or_404().db.delete(note): Đánh dấu bản ghi cần xóa.db.commit(): Thực thi câu lệnh DELETE FROM xuống DB.Trả về Response(status_code=204) (HTTP Status 204 No Content - báo hiệu xóa thành công và không cần trả về nội dung JSON nào).Tóm tắt tổng quanFile router này triển khai một bộ RESTful API chuẩn mực:
"""