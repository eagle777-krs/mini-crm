def test_register(client):
    response = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456"
    }, follow_redirects=True)
    assert b'Пользователь создан!' in response.data

def test_login(client):
    client.post("/register", data={
        "username": "testuser", "email": "test@example.com", "password": "123456"
    })
    response = client.post("/login", data={
        "username": "testuser", "password": "123456"
    }, follow_redirects=True)
    assert b'Профиль пользователя' in response.data