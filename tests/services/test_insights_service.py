from unittest.mock import MagicMock, patch
from app.services.insights_service import InsightsService

def test_upsert_insights():
    db_mock = MagicMock()
    user_id = "fake-user-id"
    insights = "These are your food insights."

    user_mock = MagicMock()
    user_mock.user.email = "user@example.com"
    db_mock.auth.get_user.return_value = user_mock
    db_mock.table.return_value.upsert.return_value.execute.return_value = None
    db_mock.rpc.return_value.execute.return_value = None
    InsightsService.upsert(db_mock, user_id, insights)
    db_mock.auth.get_user.assert_called_once_with(user_id)
    db_mock.table.return_value.upsert.assert_called_once()
    db_mock.rpc.assert_called_once()