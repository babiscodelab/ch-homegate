import itertools
from typing import Any, Union

import requests

from homegater.utils import LocationNotFoundException, convert_to_camel_case

HOUSE_CATEGORY = [
    "CHALET",
    "RUSTICO",
    "FARM_HOUSE",
    "BUNGALOW",
    "SINGLE_HOUSE",
    "ENGADINE_HOUSE",
    "BIFAMILIAR_HOUSE",
    "VILLA",
]
FLAT_CATEGORY = [
    "APARTMENT",
    "MAISONETTE",
    "DUPLEX",
    "ATTIC_FLAT",
    "ROOF_FLAT",
    "STUDIO",
    "SINGLE_ROOM",
    "TERRACE_FLAT",
    "BACHELOR_FLAT",
    "LOFT",
    "ATTIC",
    "FURNISHED_FLAT",
]


class Homegate:
    BASE_URL = "https://api.homegate.ch"

    def __init__(self, location_search_lang: str = "en"):
        """
        Initialize the Homegate client.
        search_lang (str): The language to use for search results. Can be "en", "de", "fr", or "it". Defaults to "en".
        """

        if location_search_lang not in ("en", "de", "fr", "it"):
            raise ValueError(
                "Invalid search language. Only 'en', 'de', 'fr', or 'it' are accepted."
            )
        self.search_lang = location_search_lang

    def get_geo_tags(self, location_name: str, results_count: int = 1) -> list[str]:
        """
        Retrieve geo tags based on the location name.

        Args:
            location_name (str): The name of the location to search for geo tags. Can be a Kanton name, Gemeinde name, or zip code.
            results_count (int, optional): The number of results to return. Defaults to 1.

        Returns:
            List[str]: A list of geo tags.
        """
        if not location_name:
            return ["geo-country-switzerland"]

        geo_tags_url = f"{self.BASE_URL}/geo/locations?lang={self.search_lang}&name={location_name}&size={results_count}"
        try:
            response = requests.get(geo_tags_url)
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching geo tags: {e}")
            return []

        # Check if we received results
        if response_data.get("total", 0) > 0 and "results" in response_data:
            # Extract the geo tags from the available results
            geo_tags = [
                result["geoLocation"]["id"]
                for result in response_data["results"][:results_count]
            ]
            return geo_tags
        else:
            raise LocationNotFoundException(location_name)

    def search_listings(
        self,
        *,
        offer_type: str,
        categories: list[str],
        location: Union[str, list[str]],
        sort_by: str = "dateCreated",
        sort_direction: str = "desc",
        from_index: int = 0,
        size: int = 20,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Search for listings based on various parameters.

        Args:
            offer_type (str): The type of offer (e.g., "BUY" or "RENT").
            categories (List[str]): List of categories to search within. Possible values are from HOUSE_CATEGORY or FLAT_CATEGORY.
            location (str): The name of the location to search within. Can be a Kanton name, Gemeinde name, or zip code.
            sort_by (str, optional): The field to sort by. Defaults to "dateCreated".
            sort_direction (str, optional): The direction to sort (e.g., "asc" or "desc"). Defaults to "desc".
            from_index (int, optional): The starting index for the search results. Defaults to 0.
            size (int, optional): The number of results to return. Defaults to 20.
            **kwargs: Additional search parameters.

        Returns:
            Dict[str, Any]: The search results.
        """
        if isinstance(location, str) or location is None:
            location = [location]

        geo_tags = [self.get_geo_tags(loc) for loc in location]
        geo_tags = list(itertools.chain.from_iterable(geo_tags))
        search_listings_url = f"{self.BASE_URL}/search/listings"

        # Prepare the base query
        query = {
            "query": {
                "offerType": offer_type,
                "categories": categories,
                "location": {"geoTags": geo_tags},
            },
            "sortBy": sort_by,
            "sortDirection": sort_direction,
            "from": from_index,
            "size": size,
            "trackTotalHits": True,
            "fieldset": "srp-list",
        }

        # Include any extra parameters passed as kwargs to the query.
        if kwargs:
            query["query"].update(convert_to_camel_case(kwargs))
        try:
            response = requests.post(search_listings_url, json=query)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching listings: {e}")
            return {}

    def search_buy_listings(
        self,
        *,
        location: Union[str, list[str]],
        categories: list[str] = None,
        sort_by: str = "dateCreated",
        sort_direction: str = "desc",
        from_index: int = 0,
        size: int = 20,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Search for buy listings based on various parameters.

        Args:
            location (str): The name of the location to search within. Can be a Kanton name, Gemeinde name, or zip code.
            categories (List[str], optional): List of categories to search within. Defaults to HOUSE_CATEGORY + FLAT_CATEGORY.
            sort_by (str, optional): The field to sort by. Defaults to "dateCreated".
            sort_direction (str, optional): The direction to sort (e.g., "asc" or "desc"). Defaults to "desc".
            from_index (int, optional): The starting index for the search results. Defaults to 0.
            size (int, optional): The number of results to return. Defaults to 20.
            **kwargs: Additional search parameters.

        Returns:
            Dict[str, Any]: The search results.
        """
        if categories is None:
            categories = HOUSE_CATEGORY + FLAT_CATEGORY
        return self.search_listings(
            offer_type="BUY",
            categories=categories,
            location=location,
            sort_by=sort_by,
            sort_direction=sort_direction,
            from_index=from_index,
            size=size,
            **kwargs,
        )

    def search_rent_listings(
        self,
        *,
        location: Union[str, list[str]] = None,
        categories: list[str] = None,
        sort_by: str = "dateCreated",
        sort_direction: str = "desc",
        from_index: int = 0,
        size: int = 20,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Search for rent listings based on various parameters.

        Args:
            location (str): The name of the location to search within. Can be a Kanton name, Gemeinde name, or zip code.
            categories (List[str], optional): List of categories to search within. Defaults to HOUSE_CATEGORY + FLAT_CATEGORY.
            sort_by (str, optional): The field to sort by. Defaults to "dateCreated".
            sort_direction (str, optional): The direction to sort (e.g., "asc" or "desc"). Defaults to "desc".
            from_index (int, optional): The starting index for the search results. Defaults to 0.
            size (int, optional): The number of results to return. Defaults to 20.
            **kwargs: Additional search parameters.

        Returns:
            Dict[str, Any]: The search results.
        """
        if categories is None:
            categories = HOUSE_CATEGORY + FLAT_CATEGORY
        return self.search_listings(
            offer_type="RENT",
            categories=categories,
            location=location,
            sort_by=sort_by,
            sort_direction=sort_direction,
            from_index=from_index,
            size=size,
            **kwargs,
        )

    def get_listing(self, listing_id):
        url = f"{self.BASE_URL}/listings/listing/{listing_id}?sanitize=true"
        response = requests.get(url)
        return response.json()
