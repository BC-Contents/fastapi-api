from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from model.genre_model import book_genres

class Book(Base):
    
    __tablename__ = "book"
    
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    title = Column(String(150),nullable=False,index=True)
    pages = Column(Integer,nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="SET NULL"),nullable=True)
    
    author = relationship("Author", back_populates="books")
    
    genres = relationship("Genre", secondary=book_genres, back_populates="books")
    
    def __repr__(self)->str:
        return f"<Book(id={self.id},title={self.title}, author={self.author_id})"
    