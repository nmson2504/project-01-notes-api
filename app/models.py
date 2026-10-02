from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column  

from app.database import Base  # import Base class from app/database.py


class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)


"""
SQLAlchemy là thư viện ORM (Object-Relational Mapping) và SQL Toolkit hàng đầu trong Python.Nói một cách ngắn gọn, chức năng cốt lõi của SQLAlchemy là làm cầu nối giữa code Python (hướng đối tượng) và Hệ quản trị cơ sở dữ liệu quan hệ - RDBMS (dạng bảng), giúp lập trình viên thao tác với Database mà không cần phải viết SQL thuần thủ công.

1. Các Chức Năng Chính
SQLAlchemy được chia thành 2 tầng kiến trúc chính với các chức năng riêng biệt:

A. SQLAlchemy ORM (Object-Relational Mapping) - Tầng Cao
Ánh xạ Class <-> Bảng (Table): Biến Class trong Python thành Bảng, thuộc tính thành Cột, và từng Instance (đối tượng) thành từng Dòng (Row) dữ liệu.
Quản lý trạng thái đối tượng (Unit of Work): Theo dõi mọi thay đổi của dữ liệu trong quá trình chạy ứng dụng (thêm, sửa, xóa) và tự động tạo các câu lệnh SQL tối ưu nhất để lưu vào Database khi bạn gọi session.commit().
Quản lý mối quan hệ (Relationships): Tự động xử lý các mối quan hệ phức tạp như 1 - 1, 1 - Nhiều, Nhiều - Nhiều (ForeignKey, relationship) và hỗ trợ truy vấn JOIN tự động.

B. SQLAlchemy Core - Tầng Thấp
Cung cấp các công cụ để viết SQL thuần thủ công nhưng vẫn giữ được tính năng an toàn, tối ưu và tương thích với nhiều loại Database khác nhau.
Database Abstraction Layer (Trừu tượng hóa Database): Giúp ứng dụng hoạt động độc lập với loại Database. Bạn có thể chuyển đổi từ SQLite -> PostgreSQL -> MySQL chỉ bằng việc thay đổi chuỗi kết nối (databaseURL), không cần sửa lại code truy vấn.
Quản lý kết nối (Connection Pooling): Tự động khởi tạo, tái sử dụng và giải phóng các kết nối tới Database giúp ứng dụng chạy nhanh hơn và tránh quá tải Database.



Tạo một Python class NoteModel đại diện cho bảng notes trong database."

Ta có thể hình dung:

Python                         Database
─────────────────────          ─────────────────
NoteModel              ↔       notes
    │                            │
    ├── id               ↔       id
    ├── title            ↔       title
    └── content          ↔       content

Đây chính là ORM.

ORM = Object-Relational Mapping
Biến đổi qua lại giữa object Python và row/table trong database.
---
class NoteModel(Base):
    __tablename__ = "notes"
Kế thừa Base: Nhờ kế thừa từ Base (đã khai báo bằng DeclarativeBase ở file database.py), SQLAlchemy sẽ nhận diện class này là một ORM Model. Nó biết cách ánh xạ class Python này thành một Bảng dữ liệu thực sự trong Database.

__tablename__: Biến đặc biệt của SQLAlchemy dùng để đặt tên cho bảng dưới Database.
Ý nghĩa: Khi chạy ứng dụng, SQLAlchemy sẽ tạo hoặc tìm kiếm một bảng có tên chính xác là notes trong đĩa cứng/Database.

title: Mapped[str] = mapped_column(String)
content: Mapped[str] = mapped_column(String)
Mapped[str]: Khai báo kiểu dữ liệu phía Python là chuỗi ký tự (str).
mapped_column(String): Khai báo kiểu dữ liệu tương ứng trong Database là String / VARCHAR (chuỗi văn bản).

"""