import re
from typing import Any


def convert_to_camel_case(snake_case_dict: dict[str, Any]) -> dict[str, Any]:
    """Convert snake_case keys to camelCase."""
    camel_case_dict = {}
    for key, value in snake_case_dict.items():
        camel_case_key = "".join(
            word.title() if i > 0 else word for i, word in enumerate(key.split("_"))
        )
        camel_case_dict[camel_case_key] = value
    return camel_case_dict


class LocationNotFoundException(Exception):
    """Exception raised when a location is not found."""

    def __init__(self, location: str):
        self.message = f"Location not found: {location}. Only valid homegate locations are accepted."
        super().__init__(self.message)


def _is_valid_geo_tag(location: str) -> bool:
    """
    Check if the location string is a valid homegate geo tag.
    """

    pattern = r"geo-(canton|region|zipcode|city|country)-[a-zA-Z0-9-]+"
    match = re.search(pattern, location)
    return match is not None


def _is_unique_geo_set(geo_list: list[dict]) -> bool:
    """
    geo_list: List of geo locations.
    Check if the geo_list contains actual unique locations by comparing the center lat and lon.
    """
    center_lat = {geo["geoLocation"]["center"]["lat"] for geo in geo_list}
    center_lon = {geo["geoLocation"]["center"]["lon"] for geo in geo_list}
    return 1 == len(center_lat) == len(center_lon)


def _unique_geo_set(geo_list: list[dict]) -> list[dict]:
    """
    geo_list: List of geo locations.
    Return a list of unique geo locations by comparing the center lat and lon.
    """
    seen = set()
    unique_geo_list = []
    for geo in geo_list:
        keys = (
            geo["geoLocation"]["center"]["lat"],
            geo["geoLocation"]["center"]["lon"],
        )
        if keys not in seen:
            unique_geo_list.append(geo)
            seen.add(keys)
    return unique_geo_list
