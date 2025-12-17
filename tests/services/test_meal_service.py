from unittest.mock import MagicMock, patch
from app.services.meal_service import MealService

def test_list_meals():
    db_mock = MagicMock()
    db_mock.table().select().execute.return_value.data = [
        {"id": 1, "name": "Breakfast"},
        {"id": 2, "name": "Lunch"}
    ]
    
    meals = MealService.list_meals(db_mock)
    
    assert len(meals) == 2
    assert meals[0]["name"] == "Breakfast"
    assert meals[1]["name"] == "Lunch"

@patch('app.services.food_service.FoodService.get_food')
def test_create_meal(mock_get_food):
    db_mock = MagicMock()
    payload = MagicMock()
    payload.name = "Dinner"
    payload.food_ids = [1, 2]
    payload.model_dump.return_value = {"name": "Dinner", "food_ids": [1, 2]}
    
    mock_get_food.return_value = [
        {"id": 1, "name": "Chicken"},
        {"id": 2, "name": "Rice"}
    ]
    
    db_mock.rpc().execute.return_value.data = [{"id": 3, "name": "Dinner"}]
        
    meal = MealService.create_meal(db_mock, payload)
    
    assert meal["id"] == 3
    assert meal["name"] == "Dinner"
    assert mock_get_food.call_count == 2

@patch('app.services.meal_service.MealService.get_meal_by_id')
def test_update_meal(mock_get_meal_by_id):
    mock_get_meal_by_id.return_value = {"id": 1, "name": "Breakfast"}
    db_mock = MagicMock()
    meal_id = 1
    payload = MagicMock()
    payload.name = "Brunch"
    payload.food_ids = [3]
    payload.model_dump.return_value = {"name": "Brunch", "food_ids": [3]}
    
    db_mock.rpc().execute.return_value.data = [{"id": 1, "name": "Brunch"}]
    
    updated_meal = MealService.update_meal(db_mock, meal_id, payload)
    
    assert updated_meal["name"] == "Brunch"

@patch('app.services.meal_service.MealService.get_meal_by_id')
def test_get_meal(mock_get_meal_by_id):
    mock_get_meal_by_id.return_value = {"id": 1, "name": "Lunch"}
    db_mock = MagicMock()
    meal_id = 1
    
    meal = MealService.get_meal(db_mock, meal_id)
    
    assert meal["id"] == 1
    assert meal["name"] == "Lunch"

@patch('app.services.meal_service.MealService.get_meal_by_id')
def test_delete_meal(mock_get_meal_by_id):
    mock_get_meal_by_id.return_value = {"id": 1, "name": "Dinner"}
    db_mock = MagicMock()
    meal_id = 1
    
    result = MealService.delete_meal(db_mock, meal_id)
    
    assert result is True