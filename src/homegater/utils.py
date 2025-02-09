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
