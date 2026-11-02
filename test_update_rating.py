import pytest


# ทดสอบค่าขอบเขต (Boundary Values) ในการอัปเดตเรตติ้ง: 1 และ 5 บันทึกสำเร็จ (200), 0 และ 6 ต้องถูกปฏิเสธ (400)
@pytest.mark.parametrize(
    "stars,expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ],
)
def test_update_rating_boundary(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    # อ่านข้อมูลกลับมาเพื่อยืนยันสถานะเรตติ้ง
    res_get = api.get(path, headers=auth)
    assert res_get.status_code == 200
    if expected_status == 200:
        assert res_get.json()["stars"] == stars
    else:
        # หากคำขอถูกปฏิเสธ ค่าคะแนนดาวต้องคงเดิม ไม่ถูกแก้ไข
        assert res_get.json()["stars"] == rating["stars"]
