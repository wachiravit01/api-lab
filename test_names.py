import requests

SITE = "https://quickpizza.grafana.com"


# รายการชื่อพิซซ่าต้องตอบกลับด้วยรหัส 200 และมีพิซซ่าหน้า Margherita
def test_names_are_listed():
    res = requests.get(SITE + "/api/names")
    assert res.status_code == 200
    assert "Margherita" in res.json()["names"]
