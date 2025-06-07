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


def test_update_reader_success(client, db):
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

    reader = models.Reader(
        name="Old Name",
        email="old@example.com"
    )

    db.add(reader)
    db.commit()
    db.refresh(reader)

    updated_reader = {
        "name": "New Name",
        "email": "new@example.com"
    }

    response = client.put(f"/readers/{reader.id}", json=updated_reader,  headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == updated_reader["name"]
    assert data["email"] == updated_reader["email"]


def test_delete_reader_success(client, db):
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

    reader = models.Reader(
        name="Reader Name",
        email="reader@example.com"
    )

    db.add(reader)
    db.commit()
    db.refresh(reader)

    response = client.delete(f"/readers/{reader.id}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"detail": "Reader deleted"}

    deleted_reader = db.query(models.Reader).filter(models.Reader.id == reader.id).first()
    assert deleted_reader is None
