import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}


# รายการเครื่องมือตัดพิซซ่าต้องตอบกลับด้วยรหัส 200 และแสดงเครื่องมือครบทั้ง 3 ชิ้น
def test_tools_are_listed():
    res = requests.get(SITE + "/api/tools", headers=AUTH)
    assert res.status_code == 200
    assert res.json() == {"tools": ["Knife", "Pizza cutter", "Scissors"]}
