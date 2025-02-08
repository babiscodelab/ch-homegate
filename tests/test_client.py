import pytest
from unittest.mock import MagicMock
from homegater.client import Homegate, convert_to_camel_case  # Adjust the import as needed
import requests


@pytest.fixture
def client():
    """Fixture for initializing the Homegate client."""
    return Homegate()

def test_convert_to_camel_case():
    snake_case_dict = {
        "first_key": "value1",
        "second_key": "value2",
        "another_key_here": "value3"
    }
    expected_output = {
        "firstKey": "value1",
        "secondKey": "value2",
        "anotherKeyHere": "value3"
    }
    assert convert_to_camel_case(snake_case_dict) == expected_output

def test_get_geo_tags(client, mocker):
    # Mock response for the get_geo_tags function
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "total": 2,
        "results": [{"geoLocation": {"id": "12345"}}, {"geoLocation": {"id": "67890"}}]
    }
    mocker.patch('homegater.client.requests.get', return_value=mock_response)

    geo_tags = client.get_geo_tags("Zürich", results_count=1)

    # Assert the correct URL is called
    expected_url = "https://api.homegate.ch/geo/locations?lang=en&name=Zürich&size=1"
    requests.get.assert_called_once_with(expected_url)

    # Assert that the method returns the expected geo tags
    assert geo_tags == ["12345"]

def test_search_buy_listings(client, mocker):
    # Mock response for the search_buy_listings function
    mock_response = MagicMock()
    mock_response.json.return_value = {"listings": [{"id": "1", "title": "Nice House"}]}
    mocker.patch('homegater.client.requests.post', return_value=mock_response)

    categories = ["HOUSE", "VILLA"]
    result = client.search_buy_listings(categories, 500000, "Zürich")

    # Assert that the correct payload was sent
    expected_payload = {
        "query": {
            "offerType": "BUY",
            "categories": categories,
            "purchasePrice": {"to": 500000},
            "location": {"geoTags": ["12345"]}  # Mock geo tag result
        },
        "sortBy": "listingType",
        "sortDirection": "desc",
        "from": 0,
        "size": 20,
        "trackTotalHits": True,
        "fieldset": "srp-list"
    }
    requests.post.assert_called_once_with("https://api.homegate.ch/search/listings", json=expected_payload)
    assert result == {"listings": [{"id": "1", "title": "Nice House"}]}

def test_search_rent_listings(client, mocker):
    # Mock response for the search_rent_listings function
    mock_response = MagicMock()
    mock_response.json.return_value = {"listings": [{"id": "2", "title": "Nice Apartment"}]}
    mocker.patch('homegater.client.requests.post', return_value=mock_response)

    categories = ["APARTMENT", "DUPLEX"]
    result = client.search_rent_listings(categories, 3000, "Zürich")

    # Assert that the correct payload was sent
    expected_payload = {
        "query": {
            "offerType": "RENT",
            "categories": categories,
            "monthlyRent": {"to": 3000},
            "location": {"geoTags": ["12345"]}  # Mock geo tag result
        },
        "sortBy": "listingType",
        "sortDirection": "desc",
        "from": 0,
        "size": 20,
        "trackTotalHits": True,
        "fieldset": "srp-list"
    }
    requests.post.assert_called_once_with("https://api.homegate.ch/search/listings", json=expected_payload)
    assert result == {"listings": [{"id": "2", "title": "Nice Apartment"}]}

def test_get_listing(client, mocker):
    # Mock response for the get_listing function
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "4001544515", "title": "Beautiful Villa"}
    mocker.patch('homegater.client.requests.get', return_value=mock_response)

    listing_id = "4001544515"
    result = client.get_listing(listing_id)

    # Assert the correct URL is called
    expected_url = f"https://api.homegate.ch/listings/listing/{listing_id}?sanitize=true"
    requests.get.assert_called_once_with(expected_url)

    # Assert that the method returns the expected result
    assert result == {"id": "4001544515", "title": "Beautiful Villa"}
