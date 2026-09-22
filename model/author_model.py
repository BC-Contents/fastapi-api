from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Author(Base):
    __tablename__ ="authors"
    
    id = Column(Integer,primary_key=True,index=True, autoincrement=True)
    name = Column(String(100),nullable=False,index=True)
    biography = Column(String(500),nullable=True)
    
    books = relationship("Book",back_populates="author",cascade="all, delete-orphan")
    
    def __repr__(self)->str:
        return f"<Author(id={self.id}, name='{self.name}')"