from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "notes.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import NoteModel

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        note_count = db.scalar(select(func.count()).select_from(NoteModel))
        if note_count == 0:
            db.add(
                NoteModel(
                    title="Learn FastAPI",
                    content="Understand REST API",
                )
            )
            db.commit()
    finally:
        db.close()


"""
File database.py đóng vai trò là trung tâm quản lý kết nối và khởi tạo Cơ sở dữ liệu (Database Layer) cho toàn bộ ứng dụng (thường là ứng dụng FastAPI/Flask).

Dưới đây là giải thích chi tiết mục đích và vai trò của từng thành phần trong file code của bạn:

1. Định vị và Tạo Chuỗi Kết Nối (Database Connection Setup)

DB_PATH = Path(__file__).resolve().parent.parent / "notes.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
Mục đích: Xử lý đường dẫn file cơ sở dữ liệu SQLite một cách linh hoạt.

Chi tiết:

Path(__file__).resolve().parent.parent: Định vị thư mục gốc của dự án một cách tự động (tránh lỗi "không tìm thấy file" khi chạy app từ các thư mục làm việc khác nhau).

notes.db: Tên file CSDL SQLite sẽ lưu trên đĩa cứng.

as_posix(): Chuyển đổi đường dẫn thành dạng chuẩn dùng dấu gạch chéo / (giúp code chạy tương thích trên cả Windows, Linux và macOS).

2. Khởi tạo Engine & Session Factory

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)
engine (Động cơ kết nối):

Đóng vai trò là cổng giao tiếp trực tiếp giữa Python và Database.

connect_args={"check_same_thread": False}: Cấu hình riêng cho SQLite. Theo mặc định, SQLite chỉ cho phép 1 thread truy cập. Khi dùng với các framework bất đồng bộ như FastAPI (chạy nhiều thread cùng lúc), tham số này giúp tránh lỗi kẹt thread.

SessionLocal (Nhà máy tạo Session):

Là một Class Factory. Mỗi khi gọi SessionLocal(), nó sẽ sinh ra một phiên làm việc (Session) độc lập với Database.

Mọi thao tác CRUD (Thêm, Đọc, Sửa, Xóa) sau này sẽ được thực hiện thông qua instance của Session này.

3. Khai báo Lớp Cơ Sở (Declarative Base)

class Base(DeclarativeBase):
    pass
Vai trò: Sử dụng cú pháp chuẩn mới nhất của SQLAlchemy 2.0 (DeclarativeBase).

Mục đích: Tất cả các Data Model (như NoteModel, UserModel...) sẽ kế thừa từ class Base này để SQLAlchemy có thể theo dõi, quản lý và tự động tạo bảng trong Database.

4. Hàm get_db() - Quản lý Vòng đời Session (Dependency Injection)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Mục đích: Cung cấp phiên làm việc (Database Session) cho từng Request và tự động dọn dẹp/đóng kết nối sau khi xử lý xong.

Cơ chế:

Dùng từ khóa yield để biến hàm thành một Generator.

Rất hay được dùng làm Depends(get_db) trong FastAPI. Khi nhận 1 HTTP Request, ứng dụng mở kết nối (db = SessionLocal()), cho phép xử lý dữ liệu (yield db), và ngay khi xử lý xong (dù thành công hay gặp lỗi nhờ khối finally), kết nối sẽ tự động đóng lại (db.close()) để tránh rò rỉ tài nguyên (connection leak).

5. Hàm init_db() - Khởi tạo Bảng & Dữ liệu Mẫu (Database Initialization)

def init_db():
    from app.models import NoteModel

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        note_count = db.scalar(select(func.count()).select_from(NoteModel))
        if note_count == 0:
            db.add(
                NoteModel(
                    title="Learn FastAPI",
                    content="Understand REST API",
                )
            )
            db.commit()
    finally:
        db.close()
Mục đích: Khởi tạo cấu trúc Database và nạp dữ liệu mồi (Seed Data) khi ứng dụng vừa khởi chạy.

Chi tiết từng bước:

from app.models import NoteModel: Import model bên trong hàm (Lazy Import) để đăng ký NoteModel vào Base.metadata, đồng thời tránh lỗi vòng lặp import (Circular Import).

Base.metadata.create_all(bind=engine): Quét toàn bộ các Model đã đăng ký với Base và tự động tạo các Bảng trong Database nếu chúng chưa tồn tại.

Đếm số lượng records (func.count()): Kiểm tra xem bảng notes đã có dữ liệu chưa.

Thêm dữ liệu mẫu (Seed Data): Nếu bảng đang trống (note_count == 0), tự động chèn một bản ghi ghi chú mặc định "Learn FastAPI" vào CSDL để dùng thử.

Tóm tắt tổng quan
File database.py này cung cấp một bộ giải pháp toàn diện cho Database:

- Thiết lập kết nối (engine, DATABASE_URL).
- Cung cấp công cụ quản lý dữ liệu (Base, SessionLocal).
- Cung cấp cơ chế quản lý kết nối an toàn cho API (get_db).
- Tự động chuẩn bị Database sẵn sàng sử dụng khi chạy app (init_db).
"""
