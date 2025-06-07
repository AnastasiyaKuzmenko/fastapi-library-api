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



def test_checkout_book_more_4_books(client, db):
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

    reader = models.Reader(name="John Bae", email="john@example.com")
    db.add(reader)
    db.commit()
    db.refresh(reader)

    books = []
    for i in range(4):
        book = models.Book(title=f"Test Book {i+1}", author="Author", copies_available=1)
        db.add(book)
        books.append(book)
    db.commit()
    for book in books:
        db.refresh(book)

    for i in range(3):
        response = client.post("/borrow/checkout", json={
            "book_id": books[i].id,
            "reader_id": reader.id
        },  headers=headers )
        assert response.status_code == 200


    response = client.post("/borrow/checkout", json={"book_id": books[3].id, "reader_id": reader.id}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Reader already has 3 borrowed books"    
