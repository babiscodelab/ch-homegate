import requests
import json
from typing import List, Dict, Any


def convert_to_camel_case(snake_case_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Convert snake_case keys to camelCase."""
    camel_case_dict = {}
    for key, value in snake_case_dict.items():
        camel_case_key = ''.join(word.title() if i > 0 else word for i, word in enumerate(key.split('_')))
        camel_case_dict[camel_case_key] = value
    return camel_case_dict
