from typing import List
from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.author_schema import AuthorCreate, AuthorResponse
import controller.author_controller as controller


router = APIRouter(
    prefix="/author",
    tags=["Author"]
)

@router.get(
    "/",
    response_model=List[AuthorResponse],
    summary="Read a authors",
    description="Seen all authors"
)
def read_author(
    skip:int =Query(0,ge=0,description="Number record"),
    limit:int =Query(100,ge=1, le=100,description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Author",
    description="Add a Author",
)

def create_new_author(
    author_data:AuthorCreate,
    db:Session =Depends(get_db)
):
    return controller.create_author(db=db, author_data=author_data)