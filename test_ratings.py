# เรตติ้งที่สร้างขึ้นใหม่ต้องได้รับรหัส 201 พร้อม ID (จำนวนเต็ม), คะแนนดาว และ Pizza ID ตรงตามที่ส่ง
def test_create_rating(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    body = res.json()
    assert body["stars"] == 5
    assert body["pizza_id"] == pizza_id
    assert isinstance(body["id"], int)


# เรตติ้งที่บันทึกไว้สามารถอ่านกลับมาได้ด้วย ID และได้ข้อมูลตรงกันทั้งหมด
def test_read_rating(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# การอัปเดตคะแนนดาวของเรตติ้งต้องตอบกลับด้วยคะแนนดาวค่าใหม่
def test_update_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 4}, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == 4


# เรตติ้งที่ถูกลบไปแล้ว (204) ต้องไม่สามารถอ่านได้อีก (ต้องตอบกลับด้วย 404)
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=auth)
    assert res.status_code == 204
    res = api.get(path, headers=auth)
    assert res.status_code == 404
