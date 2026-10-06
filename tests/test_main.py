from fastapi.testclient import TestClient

from app.main import app

import sys
print(sys.path)

# print(sys.path) để kiểm tra xem pytest có nhận ra thư mục gốc của dự án hay không. Nếu pytest không nhận ra thư mục gốc, sẽ báo lỗi ModuleNotFoundError: No module named 'app' khi import app.main.
# Trong pytest.ini, đã khai báo pythonpath = . để pytest nhận ra thư mục gốc của dự án. Nếu không khai báo, pytest sẽ không nhận ra thư mục gốc và báo lỗi khi import app.main.
# Kiểm tra trong terminal: dòng Collecting path của pytest có chứa đường dẫn đến thư mục gốc của dự án hay không.

'''
assert = câu lệnh dùng để khẳng định một điều kiện phải đúng. Trong pytest, assert là công cụ chính để xác định test PASS hay FAIL.

assert có thể hiểu đơn giản là:
"Tôi khẳng định rằng điều kiện này phải đúng. Nếu không đúng → báo lỗi."

Vd:
assert response.status_code == 204
Có thể đọc: "Tôi khẳng định HTTP status code phải bằng 204."
Nếu đúng, test case này PASS.
Nếu không đúng, pytest sẽ báo lỗi và test case này FAIL.
'''



client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Personal Notes API"}


def test_get_note_not_found():
    response = client.get("/notes/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note 999999 not found"}


def test_note_crud():
    # 1. CREATE
    response = client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "Created by pytest",
        },
    )

    assert response.status_code == 201

    created_note = response.json()

    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "Created by pytest"

    note_id = created_note["id"]

    # 2. READ
    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 200

    note = response.json()

    assert note["id"] == note_id
    assert note["title"] == "Test Note"
    assert note["content"] == "Created by pytest"

    # 3. UPDATE
    response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "Updated Note",
            "content": "Updated by pytest",
        },
    )

    assert response.status_code == 200

    updated_note = response.json()

    assert updated_note["id"] == note_id
    assert updated_note["title"] == "Updated Note"
    assert updated_note["content"] == "Updated by pytest"

    # 4. DELETE
    response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 204
    # Server đã thực hiện thành công nhưng không trả body.

    # 5. Verify DELETE
    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 404
    # Verify lại rằng note đã bị xóa và không còn tồn tại nữa.

def test_update_note_not_found():
    response = client.put(
        "/notes/999999",
        json={
            "title": "Updated",
            "content": "Updated content",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Note 999999 not found"}

def test_delete_note_not_found():
    response = client.delete("/notes/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note 999999 not found"}


# Hàm test cho phép in ra thông tin request và response của API khi chạy test case. Giúp debug dễ dàng hơn.
# Syntax: pytest -s
# pytest mặc định "nuốt" output của print(), phải dùng option -s để hiển thị output của print() trong quá trình chạy test case.
def test_create_note():
    payload = {
        "title": "Test",
        "content": "Hello",
    }

    response = client.post("/notes", json=payload)

    print("\n========== API TEST ==========")
    print("REQUEST")
    print("POST /notes")
    print("Body:", payload)

    print("\nRESPONSE")
    print("Status:", response.status_code)
    print("Headers:", dict(response.headers))
    print("Body:", response.json())

    print("==============================")

    assert response.status_code == 201



