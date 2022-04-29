from tests import helpers
import pytest


def test_user_fetching(db_first_user, client):
    res = client.get(f"/users/{db_first_user.id}")
    assert res.status_code == 200

    user = res.json()
    assert user["username"] is not None
    assert user["id"] is not None


def test_fetch_inexistant_user(client):
    rand_user_id = helpers.rand_uuid()
    res = client.get(f"/users/{rand_user_id}")

    assert res.status_code == 409


def test_user_follow(db_first_user, db_second_user, client):
    user_one_id = db_first_user.id
    user_two_id = db_second_user.id

    user_following_num_res = client.get(f"/users/{user_one_id}")
    user_following_num = user_following_num_res.json()["following"]

    user_to_fllw = {"followed_id": str(user_two_id)}

    res = client.post(f"/users/{user_one_id}/follow", json=user_to_fllw)
    assert res.status_code == 201

    get_user_res = client.get(f"/users/{user_one_id}")
    user = get_user_res.json()

    assert user["following"] == user_following_num + 1


def test_user_unfollow(db_first_user, db_second_user, client):
    user_one_id = db_first_user.id
    user_two_id = db_second_user.id

    user_following_num_res = client.get(f"/users/{user_one_id}")
    user_following_num = user_following_num_res.json()["following"]

    user_to_unfllw = {"followed_id": str(user_two_id)}

    res = client.delete(f"/users/{user_one_id}/follow", json=user_to_unfllw)
    assert res.status_code == 204

    get_user_res = client.get(f"/users/{user_one_id}")
    user = get_user_res.json()

    assert user["following"] == user_following_num - 1
