from typing import List
from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.book_schema import BookCreate, BookResponse
import controller.book_controller as controller


router = APIRouter(
    prefix="/book",
    tags=["Book"]
)

@router.get(
    "/",
    response_model=List[BookResponse],
    summary="Read a books",
    description="Seen all books"
)
def read_books(
    skip:int =Query(0,ge=0,description="Number record"),
    limit:int =Query(100,ge=1, le=100,description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a book",
)

def create_new_book(
    book_data:BookCreate,
    db:Session =Depends(get_db)
):
    return controller.create_book(db=db, book_data=book_data)