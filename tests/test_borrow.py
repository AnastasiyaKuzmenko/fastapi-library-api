from app import models, auth

def test_checkout_book_success(client, db):
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

    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    book = models.Book(title="Test Book", author="Author", copies_available=1)
    db.add(book)
    db.commit()
    db.refresh(book)

    reader = models.Reader(name="John Bae", email="john@example.com")
    db.add(reader)
    db.commit()
    db.refresh(reader)

    response = client.post("/borrow/checkout", json={
        "book_id": book.id,
        "reader_id": reader.id
    },  headers=headers )

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book.id
    assert data["reader_id"] == reader.id
    assert data["return_date"] is None


