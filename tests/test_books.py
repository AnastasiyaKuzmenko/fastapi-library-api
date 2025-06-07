from app import models, auth


def test_create_book_success(client, db):
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

    book_data = {
        "title": "Test Book",
        "author": "Author",
        "publication_year": 2023,
        "isbn": "123-4567890123",
        "copies_available": 1,
        "description": "Test description"
    }

    response = client.post("/books/", json=book_data,  headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["copies_available"] == book_data["copies_available"]
    assert "id" in data
