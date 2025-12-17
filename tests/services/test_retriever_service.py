from unittest.mock import MagicMock, patch
from app.services.retriever_service import RetrieverService

@patch('app.services.retriever_service.create_client')
def test_search(mock_create_client):
    db_mock = MagicMock()
    mock_create_client.return_value = db_mock
    
    query = "test query"
    
    db_mock.rpc().execute.return_value.data = [
        {"id": 1, "filename": "doc1.txt", "content": "This is a test document."},
        {"id": 2, "filename": "doc2.txt", "content": "Another test document here."}
    ]
    
    retriever = RetrieverService('fake-url', 'fake-key')
    results = retriever.search(db_mock, query)
    
    assert len(results) == 2
    assert results[0]["filename"] == "doc1.txt"
    assert results[1]["filename"] == "doc2.txt"