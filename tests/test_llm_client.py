import pytest
import responses
from src.api.llm_client import LLMClient


@pytest.fixture
def llm_client():
    """Create a test LLM client instance"""
    return LLMClient(
        base_url="https://api.example.com/v1/chat",
        api_key="test-api-key"
    )

@responses.activate
def test_successful_api_call(llm_client):
    """Test successful API call with mock response"""
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.example.com/v1/chat",
        json={"response": "Test response"},
        status=200
    )

    # Test the API call
    response = llm_client.get_response("Test prompt")
    assert response == "Test response"

@responses.activate
def test_api_call_failure(llm_client):
    """Test API call failure handling"""
    # Mock a failed API response
    responses.add(
        responses.POST,
        "https://api.example.com/v1/chat",
        json={"error": "API Error"},
        status=400
    )

    # Test error handling
    with pytest.raises(Exception) as exc_info:
        llm_client.get_response("Test prompt")
    assert "Error: 400" in str(exc_info.value)

def test_invalid_api_key():
    """Test initialization with invalid API key"""
    with pytest.raises(ValueError):
        LLMClient(base_url="https://api.example.com", api_key="")

@responses.activate
def test_request_headers(llm_client):
    """Test if correct headers are sent"""
    # Mock the API response
    def check_headers(request):
        assert request.headers['Authorization'] == 'Bearer test-api-key'
        assert request.headers['Content-Type'] == 'application/json'
        return (200, {}, '{"response": "Test response"}')

    responses.add_callback(
        responses.POST,
        "https://api.example.com/v1/chat",
        callback=check_headers
    )

    llm_client.get_response("Test prompt")