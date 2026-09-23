from typing import List
from fastapi import HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from model.genre_model import Genre
from schema.genre_schema import GenreCreate


def get_all(db:Session,skip:int = 0, limit: int = 100)->List[Genre]:
    try:
        return(
            db.query(Genre)
            .option(joinedload(Genre.books))
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating genre {str(error)}"
        )
    


def create_genre(db:Session, genre_data: GenreCreate) -> Genre:
    
    existing_genre = db.query(Genre).filter(Genre.name == genre_data.name ).first()
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name '{genre_data.name}' already exist"
        )
    
    new_genre = Genre(name = genre_data.name)
    
    try:
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
        return new_genre
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating genre {str(error)}"
        )