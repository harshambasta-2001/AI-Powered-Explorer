from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock


def get_auth_headers(client: TestClient) -> dict:
    """Helper to register and login a user to get auth headers."""
    client.post(
        "/user/register/",
        json={"email": "taskuser@example.com", "username": "taskuser", "password": "password"},
    )
    login_response = client.post(
        "/user/login/",
        json={"email": "taskuser@example.com", "password": "password"},
    )
    access_token = login_response.json()["access_token"]
    return {"token": access_token}


# Async context manager mock for streamablehttp_client
def get_async_context_manager_mock():
    mock = MagicMock()
    mock.__aenter__.return_value = (MagicMock(), MagicMock(), MagicMock())
    mock.__aexit__ = AsyncMock()
    return mock
    

def test_create_search_task(client: TestClient, mocker):
    """Test creating a search task, mocking the MCP interaction."""
    header = get_auth_headers(client)

    # Mock the MCP client
    # mock_text_content = MagicMock()
    # mock_text_content.text = "Quantum computing is a new kind of computing."
    
    # mock_result = MagicMock()
    # mock_result.content = [mock_text_content]

    # mock_session = MagicMock()
    # mock_session.call_tool = AsyncMock(return_value=mock_result)
    
    # mocker.patch("app.routes.task.ClientSession", return_value=mock_session)
    # mocker.patch("app.routes.task.streamablehttp_client", return_value=get_async_context_manager_mock())

    response = client.post(
        "/dashboard/search/",
        headers=header,
        json={"prompt_or_query": "What is quantum computing?"},
    )
    # print(response.json(),header["token"])
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Task Created Successfully"


def test_create_image_task(client: TestClient, mocker):
    """Test creating an image task, mocking the MCP interaction."""
    header = get_auth_headers(client)

    # Mock the MCP client
    # mock_image_content = MagicMock()
    # mock_image_content.text = "http://example.com/image.png"

    # mock_result = MagicMock()
    # mock_result.content = [mock_image_content]

    # mock_session = MagicMock()
    # mock_session.call_tool = AsyncMock(return_value=mock_result)

    # mocker.patch("app.routes.task.ClientSession", return_value=mock_session) # Mock ClientSession
    # mocker.patch("app.routes.task.streamablehttp_client", return_value=get_async_context_manager_mock()) # Mock streamablehttp_client as an async context manager

    response = client.post(
        "/dashboard/image/",
        headers=header,
        json={"prompt_or_query": "An astronaut on a horse"},
    )
    
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Task Created Successfully"