
from homegater.client import Homegate  # Adjust the import as needed
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def client():
    """Fixture for initializing the Homegate client."""
    return Homegate()


@pytest.fixture
def mock_geo_tag():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "total": 2,
        "results": [{"geoLocation": {"id": "12345"}}, {"geoLocation": {"id": "67890"}}]
    }
    return mock_response

@pytest.fixture
def mock_listing():
    # Mock response for the search_rent_listings function
    mock_response = MagicMock()
    mock_response.json.return_value = {"listings": [{"id": "2", "title": "Nice Apartment"}]}
    return mock_response