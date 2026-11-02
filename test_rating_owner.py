# ผู้ใช้อื่นต้องไม่สามารถอ่านเรตติ้งของเจ้าของได้ (ต้องถูกปฏิเสธด้วยรหัส 400-499)
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    # ตรวจสอบว่าเจ้าของยังสามารถอ่านเรตติ้งเดิมได้โดยข้อมูลไม่เปลี่ยนแปลง
    res_owner = api.get(path, headers=auth)
    assert res_owner.status_code == 200
    assert res_owner.json() == rating


# ผู้ใช้อื่นต้องไม่สามารถแก้ไขเรตติ้งของเจ้าของได้ (ต้องถูกปฏิเสธด้วยรหัส 400-499)
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    # ตรวจสอบว่าเรตติ้งของเจ้าของยังไม่ถูกแก้ไข
    res_owner = api.get(path, headers=auth)
    assert res_owner.status_code == 200
    assert res_owner.json() == rating


# ผู้ใช้อื่นต้องไม่สามารถลบเรตติ้งของเจ้าของได้ (ต้องถูกปฏิเสธด้วยรหัส 400-499)
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    # ตรวจสอบว่าเรตติ้งของเจ้าของยังคงอยู่ในระบบ
    res_owner = api.get(path, headers=auth)
    assert res_owner.status_code == 200
    assert res_owner.json() == rating
