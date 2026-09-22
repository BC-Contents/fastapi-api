from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class AuthorBase(BaseModel):
    
    name: str = Field(...,min_length=1,max_length=100,examples=["Miguel de Cervantes"])
    biography: Optional[str] = Field(None, max_length=500)
    
class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name:Optional[str]= Field(None,min_length=1,max_length=100)
    biography:Optional[str] = Field(None, max_length=500)
    

class AuthorResponse(AuthorBase):
    
    id:int = Field(...,description="Primary Key")
    model_config= ConfigDict(from_attributes=True)