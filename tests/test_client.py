from unittest.mock import ANY, MagicMock

import requests


def test_get_geo_tags(client, mocker, mock_geo_tag):
    # Mock response for the get_geo_tags function
    mocker.patch("homegater.client.requests.get", return_value=mock_geo_tag)

    geo_tags = client.get_geo_tags("Zürich", results_count=1)

    # Assert the correct URL is called
    expected_url = "https://api.homegate.ch/geo/locations?lang=en&name=Zürich&size=1"
    requests.get.assert_called_once_with(expected_url)

    # Assert that the method returns the expected geo tags
    assert geo_tags == ["12345"]


def test_search_buy_listings(client, mocker, mock_geo_tag):
    # Mock response for the search_buy_listings function
    mocker.patch("homegater.client.requests.get", return_value=mock_geo_tag)

    mock_response = MagicMock()
    mock_response.json.return_value = {"listings": [{"id": "1", "title": "Nice House"}]}
    mocker.patch("homegater.client.requests.post", return_value=mock_response)

    categories = ["HOUSE", "VILLA"]
    result = client.search_buy_listings(categories=categories, location="Zürich")

    # Assert that the correct payload was sent
    expected_payload = {
        "query": {
            "offerType": "BUY",
            "categories": categories,
            "location": {"geoTags": ["12345", "67890"]},  # Mock geo tag result
        },
        "sortBy": "dateCreated",
        "sortDirection": "desc",
        "from": 0,
        "size": 20,
        "trackTotalHits": True,
        "fieldset": "srp-list",
    }
    requests.post.assert_called_once_with(
        "https://api.homegate.ch/search/listings", json=expected_payload
    )
    assert result == {"listings": [{"id": "1", "title": "Nice House"}]}


def test_search_rent_listings(client, mocker, mock_geo_tag):
    mocker.patch("homegater.client.requests.get", return_value=mock_geo_tag)

    # Mock response for the search_rent_listings function
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "listings": [{"id": "2", "title": "Nice Apartment"}]
    }
    mocker.patch("homegater.client.requests.post", return_value=mock_response)

    categories = ["APARTMENT", "DUPLEX"]
    result = client.search_rent_listings(
        categories=categories, location="Zürich", monthly_rent={"to": 3000}
    )

    # Assert that the correct payload was sent
    expected_payload = {
        "query": {
            "offerType": "RENT",
            "categories": categories,
            "monthlyRent": {"to": 3000},
            "location": {"geoTags": ["12345", "67890"]},  # Mock geo tag result
        },
        "sortBy": "dateCreated",
        "sortDirection": "desc",
        "from": 0,
        "size": 20,
        "trackTotalHits": True,
        "fieldset": "srp-list",
    }
    requests.post.assert_called_once_with(
        "https://api.homegate.ch/search/listings", json=ANY
    )
    actual_payload = requests.post.call_args[1]["json"]
    assert actual_payload == expected_payload

    assert result == {"listings": [{"id": "2", "title": "Nice Apartment"}]}


def test_get_listing(client, mocker):
    # Mock response for the get_listing function
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "4001544515", "title": "Beautiful Villa"}
    mocker.patch("homegater.client.requests.get", return_value=mock_response)

    listing_id = "4001544515"
    result = client.get_listing(listing_id)

    # Assert the correct URL is called
    expected_url = (
        f"https://api.homegate.ch/listings/listing/{listing_id}?sanitize=true"
    )
    requests.get.assert_called_once_with(expected_url)

    # Assert that the method returns the expected result
    assert result == {"id": "4001544515", "title": "Beautiful Villa"}
