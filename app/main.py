from fastapi import FastAPI
from .routers import users 
#, readers, books, borrow

app = FastAPI()


app.include_router(users.router)
#app.include_router(readers.router)
#app.include_router(books.router)
#app.include_router(borrow.router)


@app.get("/")
def read_root():
    return {"message": "Library API is running"}