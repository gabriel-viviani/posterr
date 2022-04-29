import pytest

from tests.helpers import rand_giant_text, rand_small_text
from src.dto.post import PostTypes


def create_default_post(db_first_user, client):
    post_json = {
        "text": rand_small_text(),
        "author_id": db_first_user.id,
        "type": PostTypes.DEFAULT,
    }

    res = client.post(f"/posts", json=post_json)
    assert res.status_code == 201


def test_giant_text(db_first_user, client):
    post_json = {"text": rand_giant_text(), "author_id": db_first_user}

    res = client.post(f"/posts", json=post_json)
    assert res.status_code == 422


def test_create_repost(db_first_user, client):
    post_json = {
        "text": rand_small_text(),
        "author_id": db_first_user.id,
        "type": PostTypes.DEFAULT,
    }
    post_res = client.post(f"/posts", json=post_json)

    post = post_res.json()
    repost_json = {
        "referred_post_id": post["id"],
        "author_id": db_first_user.id,
        "type": PostTypes.REPOST,
    }

    repost_res = client.post(f"/posts/repost", Json=repost_json)
    repost = repost_res.json()

    assert repost_res.status_code == 201
    assert repost["id"] is not None


def test_create_quote_post(db_first_user, client):
    post_json = {
        "text": rand_small_text(),
        "author_id": db_first_user.id,
        "type": PostTypes.DEFAULT,
    }
    post_res = client.post(f"/posts", json=post_json)

    post = post_res.json()
    quote_json = {
        "quote_text": rand_small_text(),
        "referred_post_id": post["id"],
        "author_id": db_first_user.id,
        "type": PostTypes.REPOST,
    }

    quote_res = client.post(f"/posts/quote", Json=quote_json)
    quote = quote_res.json()

    assert quote_res.status_code == 201
    assert quote["id"] is not None


def test_get_all_posts(db_first_user, client):
    for i in range(3):
        post_json = {
            "text": rand_small_text(),
            "author_id": db_first_user.id,
            "type": PostTypes.DEFAULT,
        }
        client.post(f"/posts", json=post_json)

    res = client.get("/posts")
    posts = res.json()

    assert res.status_code == 200
    assert len(posts) >= 3
