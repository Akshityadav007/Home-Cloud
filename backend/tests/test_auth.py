def test_register_user(client):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"


def test_login_user(client):

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data