from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    
    title:str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Title book",
        examples=["Don Quijote"]
    )
    
    author:str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Author book",
        examples=["Miguel de Cervantes"]
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
    author:Optional[str] =Field(None,min_length=1,max_length=150)
    page:Optional[str] = Field(None, gt=0)
    is_avaible:Optional[bool] = Field(None)

    
class BookResponse(BookBase):
    
    id:int = Field(...,description="PK database", examples=[1])
    
    model_config = ConfigDict(from_attributes=True)