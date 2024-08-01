from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, HTTPException, Depends , Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db import crud, models, schemas
from db.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

username = "admin"
password = "1"

template = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.mount("/css", StaticFiles(directory="css"), name="css")

@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Ці дані доступні лише авторизованим користувачам"}

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != username or form_data.password != password:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")

    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/author-create/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db), current_user:str = Depends(protected)):
    return crud.create_author(db=db, author=author)

@app.post("/{author_id}/book-create/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db), current_user:str = Depends(protected)):
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/")
def booklist(request:Request, skip: int=0 , limit: int=50, db:Session= Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return template.TemplateResponse("main.html", {'request': request, 'books': books})

uvicorn.run(app)