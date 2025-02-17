import itertools
from typing import Any, Union

import requests

from homegater.utils import (
    LocationNotFoundException,
    _is_valid_geo_tag,
    _unique_geo_set,
    convert_to_camel_case,
)

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

    def __init__(self, location_search_lang: str = "en", max_search_geo: int = 1):
        """
        Initialize the Homegate client.
        search_lang (str): The language to use for search results. Can be "en", "de", "fr", or "it". Defaults to "en".
        max_search_geo (int): The maximum number of geo tags to search for location. Defaults to 1.
        """

        if location_search_lang not in ("en", "de", "fr", "it"):
            raise ValueError(
                "Invalid search language. Only 'en', 'de', 'fr', or 'it' are accepted."
            )
        self.location_search_lang = location_search_lang
        self.max_search_geo = max_search_geo

    def get_geo_tags(
        self, location_name: str, results_count: int = 100, unique: bool = True
    ) -> list[str]:
        """
        Retrieve geo tags based on the location name.

        Args:
            location_name (str): The name of the location to search for geo tags. Can be a Kanton name, Gemeinde name, or zip code.
            results_count (int, optional): The number of results to return. Defaults to 100.

        Returns:
            List[str]: A list of geo tags.
        """

        if not location_name:
            return ["geo-country-switzerland"]

        if _is_valid_geo_tag(location_name):
            return [location_name]

        geo_tags_url = f"{self.BASE_URL}/geo/locations?lang={self.location_search_lang}&name={location_name}&size={results_count}"
        try:
            response = requests.get(geo_tags_url)
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching geo tags: {e}") from e
        if response_data["total"] == 0:
            return LocationNotFoundException(location_name)

        if unique:
            to_return = _unique_geo_set(response_data["results"])
        else:
            to_return = response_data["results"]

        return [geo["geoLocation"]["id"] for geo in to_return]

    def search_listings(
        self,
        *,
        offer_type: str,
        categories: list[str],
        location: Union[str, list[str], dict[str, list[str]]] = None,
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

        geo_tags = []
        for loc in location:
            retrieved_geo_tags = self.get_geo_tags(loc, unique=True)
            if len(retrieved_geo_tags) > self.max_search_geo:
                raise ValueError(
                    f"{len(geo_tags)} geo-tags found with limit {self.max_search_geo} for the requested location: {loc}. "
                    "Please refine your search or incease the limit in the client. "
                    "The sugggested search way is the zip-code."
                )
            geo_tags.append(retrieved_geo_tags)

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
