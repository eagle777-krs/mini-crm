import pytest
from app.models import User, Client, Deal, DealType, db

@pytest.fixture
def user_and_client(client):
    user = User(username="salesman", email="salesman@crm.ru", password="crm")
    db.session.add(user)
    db.session.commit()

    cl = Client(name="Клиент X", email="x@x.ru", phone_number="89991110000", user_id=user.id)
    db.session.add(cl)
    db.session.commit()

    client.post("/login", data={"username": "salesman", "password": "crm"})

    return user, cl

def test_add_deal(client, user_and_client):
    _, cl = user_and_client
    response = client.post("/deal_page/add", data={
        "client_id": cl.id,
        "amount": 10000,
        "status": DealType.new.name,
        "description": "Тестовая сделка"
    }, follow_redirects=True)

    assert b"Сделка добавлен" in response.data
    assert b"Тестовая сделка" in response.data

def test_edit_deal(client, user_and_client):
    user, cl = user_and_client
    deal = Deal(client_id=cl.id, user_id=user.id, amount=5555, status=DealType.waiting, description="Редактируемая")
    db.session.add(deal)
    db.session.commit()

    response = client.post(f"/deal_page/edit/{deal.id}", data={
        "client_id": cl.id,
        "amount": 7777,
        "status": DealType.closed.name,
        "description": "Обновлено"
    }, follow_redirects=True)

    assert b"Сделка обновлена" in response.data
    assert b"Обновлено" in response.data

def test_delete_deal(client, user_and_client):
    user, cl = user_and_client
    deal = Deal(client_id=cl.id, user_id=user.id, amount=321, status=DealType.canceled, description="Удалить это")
    db.session.add(deal)
    db.session.commit()

    response = client.post(f"/deal_page/delete/{deal.id}", follow_redirects=True)
    assert b"Сделка удалена" in response.data
    assert b"Удалить это" not in response.data
