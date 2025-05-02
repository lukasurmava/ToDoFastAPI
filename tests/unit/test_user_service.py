from unittest.mock import MagicMock, patch
from app.services.user_service import user_create, read_user_by_id, user_update
from app.schemas import UserCreate, UserUpdate
from app.models import User
from fastapi import HTTPException
from app.resources.strings import USERNAME_CANT_BE_EMPTY, USER_NOT_FOUND
import pytest

@patch("app.services.user_service.insert_user")
def test_user_create_valid(mock_insert_user):
    # Arrange
    fake_user_data = UserCreate(username="testuser", email="test@example.com")
    fake_db = MagicMock()
    mock_insert_user.return_value = User(id=1, username="testuser", email="test@example.com")

    # Act
    result = user_create(fake_user_data, fake_db)

    # Assert
    assert result.username == "testuser"
    mock_insert_user.assert_called_once()


def test_user_create_empty_username():
    fake_user_data = UserCreate(username="", email="test@mail.com")
    fake_db = MagicMock()
    with pytest.raises(HTTPException) as exception:
        user_create(fake_user_data, fake_db)

    assert exception.value.status_code == 422
    assert exception.value.detail == USERNAME_CANT_BE_EMPTY


@patch("app.services.user_service.get_user_by_id")
def test_read_user_by_id(mock_get_user_by_id):
    fake_db = MagicMock()
    mock_get_user_by_id.return_value = User(id=1, username="testuser", email="test@example.com")

    result = read_user_by_id(1, fake_db)

    assert result.username == "testuser"


@patch("app.services.user_service.get_user_by_id")
def test_read_user_by_id_not_found(mock_get_user_by_id):
    fake_db = MagicMock()
    mock_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exception:
        read_user_by_id(3, fake_db)

    assert exception.value.status_code == 404
    assert exception.value.detail == USER_NOT_FOUND

@patch("app.services.user_service.update_user")
def test_user_update(mock_update_user):
    fake_user_data = UserUpdate(username="testuser", email="test@example.com")
    fake_db = MagicMock()
    mock_update_user.return_value = User(id=1, username="testuser", email="test@example.com")

    result = user_update(1, fake_user_data, fake_db)

    assert result.username == "testuser"


def test_user_update_username_empy():
    fake_user_data = UserUpdate(username="", email="test@mail.com")
    fake_db = MagicMock()
    with pytest.raises(HTTPException) as exception:
        user_update(1,fake_user_data, fake_db)

    assert exception.value.status_code == 422
    assert exception.value.detail == USERNAME_CANT_BE_EMPTY