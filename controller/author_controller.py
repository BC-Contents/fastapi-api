from typing import List
from fastapi import HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.author_model import Author
from schema.author_schema import AuthorCreate


def get_all(db:Session,skip:int = 0, limit: int = 100)->List[Author]:
    try:
        return db.query(Author).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating author {str(error)}"
        )
    


def create_author(db:Session, author_data: AuthorCreate) -> Author:
    
    new_author = Author(
        name = author_data.name,
        biography = author_data.biography
    )
    
    try:
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return new_author
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating author {str(error)}"
        )