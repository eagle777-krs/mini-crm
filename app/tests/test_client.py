import pytest
from app.models import Client, User, db

@pytest.fixture
def user(client):
    user = User(username="clientadmin", email="admin@example.com", password="adminpass")
    db.session.add(user)
    db.session.commit()
    client.post("/login", data={"username": "clientadmin", "password": "adminpass"})
    return user

def test_add_client(client, user):
    response = client.post("/client_page/add", data={
        "name": "ООО Альфа",
        "email": "client@alpha.ru",
        "phone_number": "89995553322"
    }, follow_redirects=True)
    assert b"Клиент добавлен" in response.data
    assert b"ООО Альфа" in response.data

def test_view_client(client, user):
    c = Client(name="ЗАО Бета", email="beta@corp.com", phone_number="89991112233", user_id=user.id)
    db.session.add(c)
    db.session.commit()

    response = client.get(f"/client_page/{c.id}")
    assert b"ЗАО Бета" in response.data

def test_edit_client(client, user):
    c = Client(name="Редактируемый", email="edit@corp.com", phone_number="80000000000", user_id=user.id)
    db.session.add(c)
    db.session.commit()

    response = client.post(f"/client_page/edit/{c.id}", data={
        "name": "Изменённый",
        "email": "edit@corp.com",
        "phone_number": "80000000000"
    }, follow_redirects=True)

    assert b"Клиент обновлён" in response.data
    assert b"Изменённый" in response.data

def test_delete_client(client, user):
    c = Client(name="Удаляемый", email="delete@corp.com", phone_number="8123123123", user_id=user.id)
    db.session.add(c)
    db.session.commit()

    response = client.post(f"/client_page/delete/{c.id}", follow_redirects=True)
    assert b"Клиент был удалён" in response.data
    assert b"Удаляемый" not in response.data
