from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from schema.author_schema import AuthorResponse

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
    pass

class BookUpdate(BaseModel):
    
    title:Optional[str] = Field(None,min_length=1, max_length=150)
    author_id:Optional[int] = None
    page:Optional[str] = Field(None, gt=0)
    is_avaible:Optional[bool] = Field(None)

    
class BookResponse(BookBase):
    
    id:int = Field(...,description="PK database", examples=[1])
    author: Optional[AuthorResponse] = None
    
    model_config = ConfigDict(from_attributes=True)