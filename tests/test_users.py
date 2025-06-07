from app import models, auth


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


def test_login_users_success(client, db):
    user = models.User(
        email="test@example.com",
        hashed_password=auth.get_password_hash("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post("/users/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
