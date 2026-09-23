from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from schema.book_schema import BookSimpleResponse

class GenreBase(BaseModel):
    
    name: str = Field(...,min_length=1,max_length=100,examples=["Miguel de Cervantes"])
    
class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name:Optional[str]= Field(None,min_length=1,max_length=100)
    

class GenreResponse(GenreBase):
    
    id:int = Field(...,description="Primary Key")
    model_config= ConfigDict(from_attributes=True)

class GenreDetailResponse(GenreResponse):
    books: List[BookSimpleResponse] = Field(
        default=[],
        description="List"
    )