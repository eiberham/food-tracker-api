from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService

@patch('app.services.auth_service.db')
def test_login(db_mock):
    db_mock.auth.sign_in_with_password.return_value = MagicMock(
        session=MagicMock(
            access_token="f4k3T0k3n",
            refresh_token="refr3fr35h",
            expires_in=3600,
        ),
        user=MagicMock(
            id="user-id",
            email="user@example.com",
        )
    )
    with patch('app.database.db', db_mock):
        auth_response = AuthService.login("user@example.com", "password")

    assert auth_response.access_token == "f4k3T0k3n"
    assert auth_response.refresh_token == "refr3fr35h"
    assert auth_response.expires_in == 3600
    assert auth_response.user.id == "user-id"
    assert auth_response.user.email == "user@example.com"