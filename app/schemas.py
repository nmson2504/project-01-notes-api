from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str

"""
Pydantic Schemas (thường đặt trong file schemas.py).

Trong một ứng dụng FastAPI/Python, file này đóng vai trò là Lớp bảo vệ và Kiểm duyệt dữ liệu (Data Validation & Serialization Layer) khi nhận/trả request API.

1. Phân biệt Pydantic Schema và SQLAlchemy Model
Để tránh nhầm lẫn:

SQLAlchemy Model (file models.py): Làm việc với Database (Tạo bảng, lưu xuống đĩa cứng).

Pydantic Schema (file schemas.py - code trên): Làm việc với HTTP Request / Response (Kiểm tra dữ liệu người dùng gửi lên, định dạng dữ liệu trả về client dưới dạng JSON).

2. Giải thích chi tiết từng Class
A. Class NoteCreate(BaseModel) – Dùng cho Request (Dữ liệu gửi LÊN)

class NoteCreate(BaseModel):
    title: str
    content: str
Mục đích: Dùng làm kiểu dữ liệu đầu vào cho API Tạo ghi chú mới (POST request).

Chức năng:

Validation (Kiểm tra dữ liệu): Bắt buộc người dùng phải gửi lên cả 2 trường title và content, và cả hai phải là chuỗi chữ (str). Nếu người dùng gửi thiếu hoặc sai kiểu dữ liệu, Pydantic sẽ tự động báo lỗi 422 Unprocessable Entity ngay lập tức mà chưa cần đụng tới Database.

Tự động tạo OpenAPI/Swagger Doc: FastAPI dựa vào schema này để hiển thị khung nhập dữ liệu mẫu trên trang tài liệu tương tác /docs.

Tại sao không có id? Vì khi người dùng tạo mới ghi chú, id chưa tồn tại. id sẽ do Database tự sinh ra sau này.

B. Class Note(BaseModel) – Dùng cho Response (Dữ liệu trả VỀ)

class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
Mục đích: Dùng làm kiểu dữ liệu trả về cho Client (GET/POST response) bao gồm đầy đủ thông tin: id, title, content.

Dòng cấu hình quan trọng nhất:

model_config = ConfigDict(from_attributes=True)
(Trọng Pydantic v1, cấu hình này từng được gọi là orm_mode = True).

Lý do cần dòng này: Mặc định, Pydantic chỉ hiểu dữ liệu đầu vào dưới dạng Dictionary trong Python (ví dụ: {"id": 1, "title": "abc"}).

Tuy nhiên, SQLAlchemy lại trả về kết quả dưới dạng một ORM Object (note.id, note.title - truy cập qua thuộc tính/attribute).

from_attributes=True cho phép Pydantic đọc trực tiếp các thuộc tính từ đối tượng SQLAlchemy và tự động chuyển đổi (serialize) nó thành dạng JSON để trả về cho trình duyệt/mạng.

Tóm tắt luồng hoạt động thực tế trong FastAPI
Client gửi dữ liệu lên (POST /notes):
    Pydantic dùng NoteCreate để kiểm tra: title và content có hợp lệ không?
Lưu vào Database:
    FastAPI chuyển dữ liệu sang SQLAlchemy Model (NoteModel) để lưu vào Database. Database tự sinh ra id = 1.
Trả kết quả về cho Client:
    FastAPI lấy đối tượng NoteModel từ Database, đưa qua Pydantic schema Note (from_attributes=True hoạt động tại đây) để đóng gói thành JSON { "id": 1, "title": "...", "content": "..." } trả về cho Client.
"""