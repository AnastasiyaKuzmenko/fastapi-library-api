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


def test_update_book_success(client, db):
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

    book = models.Book(
        title="Test Book",
        author="Author",
        publication_year=2023,
        isbn="123-4567890123",
        copies_available=4,
        description="Test description"
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    updated_book = {
        "title": "updated Test Book",
        "author": "updated Author",
        "publication_year": 2024,
        "isbn": "111-4567890123",
        "copies_available": 2,
        "description": "updated Test description"
    }

    response = client.put(f"/books/{book.id}", json=updated_book,  headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == updated_book["title"]
    assert data["author"] == updated_book["author"]
    assert data["publication_year"] == updated_book["publication_year"]
    assert data["isbn"] == updated_book["isbn"]
    assert data["copies_available"] == updated_book["copies_available"]
    assert data["description"] == updated_book["description"]
