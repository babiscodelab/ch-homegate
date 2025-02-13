from unittest.mock import MagicMock

import pytest

from homegater.client import Homegate  # Adjust the import as needed


@pytest.fixture
def client():
    """Fixture for initializing the Homegate client."""
    return Homegate(max_search_geo=10000)


@pytest.fixture
def client_default():
    return Homegate()


@pytest.fixture
def mock_geo_tag():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "total": 2,
        "results": [{"geoLocation": {"id": "12345"}}, {"geoLocation": {"id": "67890"}}],
    }
    return mock_response


@pytest.fixture
def mock_listing():
    # Mock response for the search_rent_listings function
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "listings": [{"id": "2", "title": "Nice Apartment"}]
    }
    return mock_response


# Fixture to mock multiple endpoints using a dictionary
@pytest.fixture
def mock_geo_request_single_response(client, requests_mock):
    response = {
        "total": 2,
        "results": [{"geoLocation": {"id": "12345"}}, {"geoLocation": {"id": "67890"}}],
    }
    requests_mock.get(f"{client.BASE_URL}/{endpoint}", json=response)


# Fixture to mock multiple endpoints using a dictionary
@pytest.fixture
def mock_geo_request_double_response(requests_mock):
    endpoints = {
        "data1": {"id": 1, "name": "Test1"},
        "data2": {"id": 2, "name": "Test2"},
        "data3": {"id": 3, "name": "Test3"},
        "data4": {"id": 4, "name": "Test4"},
        "data5": {"id": 5, "name": "Test5"},
    }

    for endpoint, response in endpoints.items():
        requests_mock.get(f"https://api.example.com/{endpoint}", json=response)
