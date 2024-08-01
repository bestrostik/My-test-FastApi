from sqlalchemy.orm import Session
from db import models, schemas

def get_authors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, second_name=author.second_name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()

def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(name=book.name, pages=book.pages, author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.DBBook).offset(skip).limit(limit).all()