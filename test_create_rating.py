import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 ดาว (จำนวนเต็ม), พิซซ่าที่มีอยู่จริง, ใช้ Token ของผู้ใช้ตนเอง
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: คะแนนดาวที่ต่ำกว่า 1 หรือมากกว่า 5 ต้องถูกปฏิเสธด้วยรหัส 400 พร้อมข้อความแจ้งเตือน
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: คะแนนดาวที่เป็นเลขทศนิยม (Decimal) ต้องถูกปฏิเสธด้วยรหัส 400
def test_stars_decimal(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    }


# C2: คะแนนดาวที่เป็นข้อความ (String) ต้องถูกปฏิเสธด้วยรหัส 400
def test_stars_text(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    }


# C2: คำขอที่ไม่ระบุฟิลด์ stars (Missing) ต้องถูกปฏิเสธด้วยรหัส 400
def test_stars_missing(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: พิซซ่าที่ไม่มีอยู่จริงในระบบ ต้องถูกปฏิเสธด้วยรหัส 400
def test_pizza_does_not_exist(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: คำขอที่ไม่แนบ Header Token ต้องถูกปฏิเสธด้วยรหัส 401
def test_token_missing(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# C4: คำขอที่แนบ Token ที่ความยาวไม่ถูกต้อง ต้องถูกปฏิเสธด้วยรหัส 401
def test_token_wrong_length(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers={"Authorization": "token short"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
