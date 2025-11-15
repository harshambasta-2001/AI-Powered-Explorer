from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user(client: TestClient):
    response = client.post(
        "/user/register/",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User Created Successfully"}


def test_login_for_access_token(client: TestClient, db_session: Session):
    # First, create a user to login with
    client.post(
        "/user/register/",
        json={"email": "login@example.com", "username": "loginuser", "password": "password123"},
    )

    response = client.post(
        "/user/login/",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/user/login/",
        json={"email": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid Credentials"}