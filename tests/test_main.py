from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_register_user():
    # Define a sample user data
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123",
    }

    # Send a POST request to the register endpoint
    response = client.post("/register", json=user_data)

    # Check if the response was successful
    assert response.status_code == 201

    # Check if the response contains the expected data
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]

    # Check if the user was actually created
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["username"] == user_data["username"]