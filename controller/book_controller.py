from typing import List
from fastapi import HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.book_model import Book
from schema.book_schema import BookCreate
from model.genre_model import Genre


def get_all(db:Session,skip:int = 0, limit: int = 100)->List[Book]:
    try:
        return db.query(Book).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating book {str(error)}"
        )
    


def create_book(db:Session, book_data: BookCreate) -> Book:
    
    new_book = Book(
        title=book_data.title,
        author_id=book_data.author_id,
        pages=book_data.pages,
        is_available=book_data.is_available
    )
    
    if book_data.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(book_data.genre_ids)).all()
        new_book.genres = genres
    
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating book {str(error)}"
        )