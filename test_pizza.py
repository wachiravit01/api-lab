import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}


# คำขอพิซซ่ามังสวิรัติต้องได้รับพิซซ่าที่มีชื่อ และทุกส่วนผสมต้องเป็นมังสวิรัติ (vegetarian == True)
def test_vegetarian_pizza():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN, headers=AUTH)
    assert res.status_code == 200
    body = res.json()
    assert body["pizza"]["name"] != ""
    for ingredient in body["pizza"]["ingredients"]:
        assert ingredient["vegetarian"] is True, ingredient["name"]


# คำขอที่ไม่แนบ Token ต้องถูกปฏิเสธด้วยรหัส 401 และข้อความ authentication failed
def test_pizza_without_token_is_refused():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
