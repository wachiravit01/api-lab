import uuid


# ผู้ใช้คนที่สองที่ใช้ชื่อซ้ำกับชื่อที่มีอยู่แล้ว ต้องถูกปฏิเสธด้วยรหัส 400 และข้อความ username already taken
def test_duplicate_username_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201
    res2 = api.post("/api/users", json=user)
    assert res2.status_code == 400
    assert res2.json() == {"error": "username already taken"}


# การล็อกอินด้วยรหัสผ่านที่ไม่ถูกต้อง ต้องถูกปฏิเสธด้วยรหัส 401 และข้อความ authentication failed
def test_wrong_password_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201
    wrong_login = {"username": name, "password": "WrongPassword123"}
    res2 = api.post("/api/users/token/login", json=wrong_login)
    assert res2.status_code == 401
    assert res2.json() == {"error": "authentication failed"}


# การสมัครสมาชิกด้วยชื่อผู้ใช้ที่ว่างเปล่า ต้องถูกปฏิเสธด้วยรหัส 400 และข้อความ username field is empty
def test_empty_username_refused(api):
    user = {"username": "", "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
