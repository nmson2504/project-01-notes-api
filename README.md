# Personal Notes API

A small REST API for managing personal notes.

Chưa sửa main.py.

Do đó notes.py mới chỉ được tạo ra, nhưng main.py chưa include router này.

Vì vậy đừng xóa các endpoint /notes trong main.py và cũng chưa cần test lại toàn bộ API lúc này.

Bước tiếp theo của chúng ta sẽ là 7C: tạo app/services/note_service.py

**Planned stack:** Python, FastAPI, SQLite, SQLAlchemy

The finished API will let you create, read, update, and delete notes over HTTP. Notes will be stored locally in SQLite. This step only sets up Git-friendly project files; application code comes later.

------------
Active venv
.\venv\Scripts\Activate.ps1

Uvirorn
uvicorn main:app --reload

Run Active venv & uvicorn
.venv\Scripts\uvicorn app.main:app --reload
(path: app/main.py)

Or
.\venv\Scripts\Activate.ps1; uvicorn main:app --reload

Or
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& k:\son\AI-Systems\project-00-notes-api\.venv\Scripts\Activate.ps1)
Explain:
1. Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Mục đích: Cấp quyền cho phép chạy các script PowerShell (file .ps1).
Chi tiết:
-Scope Process: Chỉ áp dụng chính sách này cho phiên làm việc hiện tại (cửa sổ Terminal/PowerShell đang mở). Khi bạn tắt cửa sổ này đi, thiết lập sẽ tự mất và không làm ảnh hưởng đến bảo mật chung của hệ thống Windows.
-ExecutionPolicy RemoteSigned: Cho phép chạy các script do bạn tự tạo ở máy cục bộ (local). Các script tải từ Internet về thì phải có chữ ký số an toàn mới được chạy.

2. & k:\son\AI-Systems\project-00-notes-api\.venv\Scripts\Activate.ps1
Mục đích: Kích hoạt môi trường ảo Python (Virtual Environment).
Chi tiết:
& (Call operator): Dùng để thực thi một file script hoặc lệnh theo đường dẫn.
...\.venv\Scripts\Activate.ps1: Đường dẫn tới file kích hoạt môi trường ảo Python của dự án project-00-notes-api.
Sau khi chạy xong, bạn sẽ thấy tên môi trường (.venv) xuất hiện ở đầu dòng lệnh. Tất cả các thư viện Python bạn cài đặt (pip install) hoặc thực thi (python main.py) sau đó sẽ nằm riêng biệt trong môi trường này, không làm xung đột với Python toàn hệ thống.

Tóm lại
Chuỗi lệnh này giúp bạn mở quyền chạy script cho phiên làm việc hiện tại và kích hoạt môi trường ảo Python của dự án một cách an toàn mà không cần thay đổi cấu hình bảo mật vĩnh viễn của Windows.

(Chú ý: trong môi trường Git Bash / Linux / CMD cú pháp sẽ có khác biệt)