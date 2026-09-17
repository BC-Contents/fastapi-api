from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base

class Book(Base):
    
    __tablename__ = "book"
    
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    title = Column(String(150),nullable=False,index=True)
    author = Column(String(100),nullable=False,index=True)
    pages = Column(Integer,nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self)->str:
        return f"<Book(id={self.id},title={self.title}, author={self.author})"
    