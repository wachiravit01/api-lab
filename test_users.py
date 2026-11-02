# ผู้ใช้ใหม่สามารถล็อกอินได้สำเร็จ และเริ่มต้นโดยยังไม่มีรายการเรตติ้ง (ratings ว่างเปล่า)
def test_new_user_has_no_ratings(api, auth):
    res = api.get("/api/ratings", headers=auth)
    assert res.status_code == 200
    assert res.json() == {"ratings": []}
