import pytest
from app.models import Deal, Client, User, db
from sqlalchemy import func

@pytest.fixture
def setup_deals(client):
    u = User(username="analyst", email="a@a.a", password="123")
    db.session.add(u)
    db.session.commit()

    c = Client(name="Тест Клиент", email="client@test.ru", phone_number="123", user_id=u.id)
    db.session.add(c)
    db.session.commit()

    d1 = Deal(user_id=u.id, client_id=c.id, amount=1000, status="closed")
    d2 = Deal(user_id=u.id, client_id=c.id, amount=2000, status="closed")
    db.session.add_all([d1, d2])
    db.session.commit()

    client.post("/login", data={"username": "analyst", "password": "123"})
    return u, c

def test_analytics_page(client, setup_deals):
    response = client.get("/analytics")
    assert b"Общая аналитика" in response.data
    assert b"Топ-5 клиентов" in response.data
    assert b"Сделки по месяцам" in response.data