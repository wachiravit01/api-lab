import pytest


# พิซซ่าที่สุ่มได้ต้องไม่ใช้เครื่องมือที่ลูกค้าตัดออก (Excluded Tools)
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"],
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Defect 1: การตัดเครื่องมือออกครบทั้ง 3 ชิ้น เซิร์ฟเวอร์ตอบกลับด้วย 500 แทนที่จะเป็น 400 พร้อมข้อความแจ้งเตือน JSON
@pytest.mark.xfail(
    reason="Defect 1: Excluding all tools returns 500 Internal Server Error instead of 400 Bad Request with JSON error message",
    strict=True,
)
def test_excluding_all_tools_refused_with_400(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
