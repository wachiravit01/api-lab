import uuid
import pytest
import requests

SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    """Session สำหรับเพิ่ม Base URL ของ QuickPizza อัตโนมัติในทุกเส้นทางคำขอ"""

    def request(self, method, url, *args, **kwargs):
        return super().request(method, SITE + url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    """Fixture ให้บริการ Session ร่วมกันตลอดการรัน เพื่อรักษาคุกกี้ AWSALB (Sticky Session)"""
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    """สร้างบัญชีผู้ใช้ใหม่ด้วยชื่อสุ่ม ทำการล็อกอิน และส่งคืน Header Authorization พร้อม Token"""
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    res = api.post("/api/users/token/login", json=user)
    assert res.status_code == 200
    return {"Authorization": "token " + res.json()["token"]}


@pytest.fixture
def auth(api):
    """Fixture สร้างและล็อกอินผู้ใช้ใหม่สำหรับแต่ละเทสต์"""
    return log_in_new_user(api)


@pytest.fixture
def other_auth(api):
    """Fixture สร้างและล็อกอินผู้ใช้คนที่สอง สำหรับทดสอบการเข้าถึงข้ามบัญชี"""
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    """Fixture สุ่มสร้างพิซซ่าขึ้นมา 1 ถาด และส่งคืน pizza ID"""
    res = api.post("/api/pizza", json={}, headers=auth)
    assert res.status_code == 200
    return res.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    """Fixture สร้างเรตติ้ง 3 ดาวก่อนเริ่มเทสต์ และลบทิ้ง (Teardown) หลังจบเทสต์"""
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    made = res.json()
    yield made
    api.delete(f"/api/ratings/{made['id']}", headers=auth)
