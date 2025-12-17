from unittest.mock import MagicMock, patch
from app.services.symptom_service import SymptomService

def test_list_symptoms():
    db_mock = MagicMock()
    db_mock.table().select().execute.return_value.data = [
        {"id": 1, "symptom_type": "Nausea"},
        {"id": 2, "symptom_type": "Headache"}
    ]
    
    symptoms = SymptomService.list_symptoms(db_mock)
    
    assert len(symptoms) == 2
    assert symptoms[0]["symptom_type"] == "Nausea"
    assert symptoms[1]["symptom_type"] == "Headache"

@patch('app.services.meal_service.MealService.get_meal_by_id')
def test_create_symptom(mock_get_meal_by_id):
    mock_get_meal_by_id.return_value = {"id": 1, "name": "Breakfast"}
    
    db_mock = MagicMock()
    payload = MagicMock()
    payload.meal_id = 1
    payload.datetime = None
    payload.symptom_type = "Fatigue"
    payload.severity = 3
    payload.notes = "Felt tired after meal"
    
    db_mock.rpc().execute.return_value.data = [{"id": 1, "symptom_type": "Fatigue"}]
        
    symptom = SymptomService.create_symptom(db_mock, payload)
    
    assert symptom["id"] == 1
    assert symptom["symptom_type"] == "Fatigue"
    mock_get_meal_by_id.assert_called_once_with(db_mock, 1)

@patch('app.services.symptom_service.SymptomService.get_symptom_by_id')
def test_update_symptom(mock_get_symptom_by_id):
    mock_get_symptom_by_id.return_value = {
        "id": 1,
        "datetime": None,
        "symptom_type": "Nausea",
        "severity": 2,
        "notes": "Mild nausea",
        "meal_id": 1
    }
    
    db_mock = MagicMock()
    symptom_id = 1
    payload = MagicMock()
    payload.datetime = None
    payload.symptom_type = "Severe Nausea"
    payload.severity = 5
    payload.notes = "Very bad nausea"
    payload.meal_id = 2
    
    db_mock.rpc().execute.return_value.data = [{"id": 1, "symptom_type": "Severe Nausea"}]
    
    updated_symptom = SymptomService.update_symptom(db_mock, symptom_id, payload)
    
    assert updated_symptom["symptom_type"] == "Severe Nausea"

@patch('app.services.symptom_service.SymptomService.get_symptom_by_id')
def test_get_symptom(mock_get_symptom_by_id):
    mock_get_symptom_by_id.return_value = {"id": 1, "symptom_type": "Headache"}
    db_mock = MagicMock()
    symptom_id = 1
    
    symptom = SymptomService.get_symptom_by_id(db_mock, symptom_id)
    
    assert symptom["id"] == 1
    assert symptom["symptom_type"] == "Headache"

@patch('app.services.symptom_service.SymptomService.get_symptom_by_id')
def test_delete_symptom(mock_get_symptom_by_id):
    mock_get_symptom_by_id.return_value = {"id": 1, "symptom_type": "Fatigue"}
    db_mock = MagicMock()
    symptom_id = 1
    
    result = SymptomService.delete_symptom(db_mock, symptom_id)
    
    assert result is True
    db_mock.table().delete().eq().execute.assert_called_once()