from app import models, auth


def test_create_reader_success(client, db):
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
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    reader_data = {
        "name": "Test Reader",
        "email": "reader@example.com"
    }

    response = client.post("/readers/", json=reader_data,  headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Reader"
    assert data["email"] == "reader@example.com"

