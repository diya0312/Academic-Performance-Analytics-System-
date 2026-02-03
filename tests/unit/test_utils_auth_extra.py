import builtins
import pytest
from unittest.mock import patch, MagicMock
from src.backend.utils.auth import get_user_role, require_role, valid_student

# ---- Test get_user_role ----
def test_get_user_role_found():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("admin",)
    mock_db.cursor.return_value = mock_cursor

    with patch("src.backend.utils.auth.get_db", return_value=mock_db):
        assert get_user_role("alice") == "admin"

def test_get_user_role_not_found():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db.cursor.return_value = mock_cursor

    with patch("src.backend.utils.auth.get_db", return_value=mock_db):
        assert get_user_role("ghost") is None

# ---- Test require_role ----
def test_require_role_success():
    with patch("src.backend.utils.auth.session", {"username": "alice"}):
        with patch("src.backend.utils.auth.get_user_role", return_value="admin"):
            assert require_role(["admin"]) is True

def test_require_role_no_session():
    with patch("src.backend.utils.auth.session", {}):
        with pytest.raises(Exception):
            require_role(["admin"])

def test_require_role_wrong_role():
    with patch("src.backend.utils.auth.session", {"username": "alice"}):
        with patch("src.backend.utils.auth.get_user_role", return_value="student"):
            with pytest.raises(Exception):
                require_role(["admin"])

# ---- Test valid_student ----
def test_valid_student_true():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("student",)
    mock_db.cursor.return_value = mock_cursor

    with patch("src.backend.utils.auth.get_db", return_value=mock_db):
        assert valid_student("s1") is True

def test_valid_student_false_role():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("admin",)
    mock_db.cursor.return_value = mock_cursor

    with patch("src.backend.utils.auth.get_db", return_value=mock_db):
        assert valid_student("adminuser") is False

def test_valid_student_no_user():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db.cursor.return_value = mock_cursor

    with patch("src.backend.utils.auth.get_db", return_value=mock_db):
        assert valid_student("ghost") is False
