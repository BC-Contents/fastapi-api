from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from schema.author_schema import AuthorResponse
from schema.genre_schema import GenreResponse

class BookBase(BaseModel):
    
    title:str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Title book",
        examples=["Don Quijote"]
    )
    
    author_id:Optional[int] = Field(
        default=None, description="ID of author"
    )
    
    pages: Optional[int] = Field(
        None,
        gt=0,
        description="Total pages book",
        examples=[850]
    )
    
    is_available: bool = Field(
        default=True,
        description="The book is in stock",
        examples=[True]
    )
    
class BookCreate(BookBase):
    genre_ids:Optional[List[int]] = Field(
        default=[],
        description="List id of genres",
        examples=[[1,2]]
    )
    pass

class BookUpdate(BaseModel):
    
    title:Optional[str] = Field(None,min_length=1, max_length=150)
    author_id:Optional[int] = None
    genre_ids:Optional[List[int]] = Field(
            None,
            description="Update List id of genres",
    )
    page:Optional[str] = Field(None, gt=0)
    is_avaible:Optional[bool] = Field(None)

class BookSimpleResponse(BookBase):
    
    id:int = Field(...,description="PK database", examples=[1])
    
    model_config = ConfigDict(from_attributes=True)

class BookResponse(BookSimpleResponse):
  
    author: Optional[AuthorResponse] = None
    genres: List[GenreResponse] = []
    
    model_config = ConfigDict(from_attributes=True)