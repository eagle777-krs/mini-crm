import pytest
from app.models import User, db

@pytest.fixture
def new_user():
    user = User(username="tester", email="tester@example.com", password="secret")
    db.session.add(user)
    db.session.commit()
    return user


def test_user_model(new_user):
    assert new_user.id is not None
    assert new_user.username == "tester"
    assert new_user.email == "tester@example.com"
    assert str(new_user).startswith("<User(id=")


def test_user_page_requires_login(client):
    response = client.get("/user_page/1", follow_redirects=True)
    assert b"Вход в систему" in response.data


def test_user_page_authenticated(client, new_user):
    # логинимся
    response = client.post("/login", data={
        "username": "tester",
        "password": "secret"
    }, follow_redirects=True)

    response = client.get(f"/user_page/{new_user.id}", follow_redirects=True)
    assert b"Профиль пользователя" in response.data
    assert bytes(new_user.username, "utf-8") in response.data