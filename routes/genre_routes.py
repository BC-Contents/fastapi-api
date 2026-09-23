from typing import List
from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.genre_schema import GenreCreate, GenreResponse, GenreDetailResponse
import controller.genre_controller as controller


router = APIRouter(
    prefix="/genre",
    tags=["Genre"]
)

@router.get(
    "/",
    response_model=List[GenreDetailResponse],
    summary="Read a genres",
    description="Seen all genres"
)
def read_genre(
    skip:int =Query(0,ge=0,description="Number record"),
    limit:int =Query(100,ge=1, le=100,description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new genre",
    description="Add a genre",
)

def create_new_genre(
    genre_data:GenreCreate,
    db:Session =Depends(get_db)
):
    return controller.create_genre(db=db, genre_data=genre_data)