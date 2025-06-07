from app import models


def test_register_users_success(client, db):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]

    user_in_db = db.query(models.User).filter(models.User.email == user_data["email"]).first()
    assert user_in_db is not None
