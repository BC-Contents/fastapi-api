import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from controller.book_controller import create_book
from model.book_model import Book
from schema.book_schema import BookCreate

def test_create_sucess():
    """ Arrange """
    db_mock= MagicMock()
    
    book_data = BookCreate(
        title="Cien años de soledad",
        author_id=1,
        pages=417,
        is_available=True,
        genre_ids=[]
    )
    
    """ Act """
    result = create_book(db=db_mock,book_data=book_data)
    
    """ Assert """
    db_mock.add.assert_called_once_with(result)
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(result)
    
    assert isinstance(result, Book)
    assert result.title == "Cien años de soledad"
    assert result.author_id == 1
    assert result.pages == 417
    assert result.is_available is True
    
def test_create_db_error():
    """ Arrange """
    db_mock_error= MagicMock()
    db_mock_error.commit.side_effect = SQLAlchemyError("Error de conexión con la base de datos")
    
    book_data = BookCreate(
        title="Libro fallo",
        author_id=1,
        pages=417,
        is_available=True,
        genre_ids=[]
    )
    
    with pytest.raises(HTTPException) as exc_info:
        create_book(db=db_mock_error, book_data=book_data)
    
    db_mock_error.rollback.assert_called_once()
    
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Database error in creating book" in exc_info.value.detail
    
    