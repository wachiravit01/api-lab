import pytest


# Boundary values for updating a rating: 1 and 5 are valid (200), 0 and 6 are refused (400).
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

    # Read back to verify rating state
    res_get = api.get(path, headers=auth)
    assert res_get.status_code == 200
    if expected_status == 200:
        assert res_get.json()["stars"] == stars
    else:
        # A refused update must leave the rating as it was
        assert res_get.json()["stars"] == rating["stars"]
