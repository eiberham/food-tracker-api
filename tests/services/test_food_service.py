from unittest.mock import MagicMock, patch
from app.services.food_service import FoodService

def test_list_foods():
    db_mock = MagicMock()
    db_mock.table().select().execute.return_value.data = [{"id": 1, "name": "Apple"}, {"id": 2, "name": "Banana"}]
    
    foods = FoodService.list_foods(db_mock)
    
    assert len(foods) == 2
    assert foods[0]["name"] == "Apple"
    assert foods[1]["name"] == "Banana"

@patch('app.services.food_service.FoodService.get_food_by_name')
def test_create_food(mock_get_food_by_name):
    mock_get_food_by_name.return_value = None
    
    db_mock = MagicMock()
    payload = MagicMock()
    payload.name = "Orange"
    payload.model_dump.return_value = {"name": "Orange"}
    
    db_mock.table().insert().select().execute.return_value = {"id": 3, "name": "Orange"}
    
    food = FoodService.create_food(db_mock, payload)

    mock_get_food_by_name.assert_called_once_with(db_mock, "Orange")
    assert food["id"] == 3
    assert food["name"] == "Orange"

@patch('app.services.food_service.FoodService.get_food_by_id')
def test_update_food(mock_get_food_by_id):
    mock_get_food_by_id.return_value = {"id": 1, "name": "Apple"}
    db_mock = MagicMock()
    food_id = 1
    payload = MagicMock()
    payload.model_dump.return_value = {"name": "Green Apple"}
    
    db_mock.table().update().eq().select().execute.return_value = {"id": 1, "name": "Green Apple"}
    
    updated_food = FoodService.update_food(db_mock, food_id, payload)
    print(updated_food)
    
    assert updated_food["name"] == "Green Apple"

@patch('app.services.food_service.FoodService.get_food_by_id')
def test_get_food(mock_get_food_by_id):
    mock_get_food_by_id.return_value = {"id": 1, "name": "Apple"}
    db_mock = MagicMock()
    food_id = 1
    
    food = FoodService.get_food(db_mock, food_id)
    
    assert food["id"] == 1
    assert food["name"] == "Apple"


@patch('app.services.food_service.FoodService.get_food_by_id')
def test_delete_food(mock_get_food_by_id):
    mock_get_food_by_id.return_value = {"id": 1, "name": "Apple"}
    db_mock = MagicMock()
    food_id = 1

    db_mock.table().delete().eq().execute().return_value = None

    success = FoodService.delete_food(db_mock, food_id)

    assert success is True
    mock_get_food_by_id.assert_called_once_with(db_mock, food_id)