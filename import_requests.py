import requests
import json

def convert_to_camel_case(snake_case_dict):
    """Convert snake_case keys to camelCase."""
    camel_case_dict = {}
    for key, value in snake_case_dict.items():
        camel_case_key = ''.join(word.title() if i > 0 else word for i, word in enumerate(key.split('_')))
        camel_case_dict[camel_case_key] = value
    return camel_case_dict

class HomegateClient:
    BASE_URL = "https://api.homegate.ch"
    
    def __init__(self):
        pass

    def get_geo_tags(self, location_name: str):
        """Retrieve geo tags based on the location name."""
        url = f"{self.BASE_URL}/geo/locations?lang=en&name={location_name}&size=1"
        response = requests.get(url)
        response_data = response.json()
        
        # Check if we received results
        if response_data.get("total", 0) > 0 and "results" in response_data:
            # Extract the geo tag from the first result
            geo_tag = response_data["results"][0]["geoLocation"]["id"]
            return [geo_tag]
        return []

    def search_buy_listings(self, categories, price_limit, location_name, sort_by="listingType", sort_direction="desc", from_index=0, size=20, **kwargs):
        geo_tags = self.get_geo_tags(location_name)
        url = f"{self.BASE_URL}/search/listings"
        
        # Prepare the base query
        query = {
            "query": {
                "offerType": "BUY",
                "categories": categories,
                "purchasePrice": {"to": price_limit},
                "location": {"geoTags": geo_tags}
            },
            "sortBy": sort_by,
            "sortDirection": sort_direction,
            "from": from_index,
            "size": size,
            "trackTotalHits": True,
            "fieldset": "srp-list"
        }

        # Include any extra parameters passed as kwargs
        if kwargs:
            query.update(convert_to_camel_case(kwargs))

        response = requests.post(url, json=query)
        return response.json()

    def search_rent_listings(self, categories, price_limit, location_name=None, exclude_categories=None, sort_by="listingType", sort_direction="desc", from_index=0, size=20, **kwargs):
        geo_tags = self.get_geo_tags(location_name) if location_name else []
        url = f"{self.BASE_URL}/search/listings"
        
        # Prepare the base query
        query = {
            "query": {
                "offerType": "RENT",
                "categories": categories,
                "monthlyRent": {"to": price_limit},
                "location": {"geoTags": geo_tags},
                "excludeCategories": exclude_categories if exclude_categories else []
            },
            "sortBy": sort_by,
            "sortDirection": sort_direction,
            "from": from_index,
            "size": size,
            "trackTotalHits": True,
            "fieldset": "srp-list"
        }

        # Include any extra parameters passed as kwargs
        if kwargs:
            query.update(convert_to_camel_case(kwargs))

        response = requests.post(url, json=query)
        return response.json()

    def get_listing(self, listing_id):
        url = f"{self.BASE_URL}/listings/listing/{listing_id}?sanitize=true"
        response = requests.get(url)
        return response.json()

# Example usage:
if __name__ == "__main__":
    client = HomegateClient()

    # Search for properties to buy with an extra parameter
    buy_categories = ["HOUSE", "ROW_HOUSE", "BIFAMILIAR_HOUSE", "TERRACE_HOUSE", "VILLA"]
    buy_listings = client.search_buy_listings(buy_categories, 5000000, "Kanton Zürich", extraParam="example")
    print(json.dumps(buy_listings, indent=2))

    # Get a specific listing
    listing_id = 4001544515
    listing_details = client.get_listing(listing_id)
    print(json.dumps(listing_details, indent=2))

    # Search for properties to rent with an extra parameter
    rent_categories = ["APARTMENT", "MAISONETTE", "DUPLEX", "ATTIC_FLAT", "ROOF_FLAT"]
    rent_listings = client.search_rent_listings(rent_categories, 10000, "Thalwil", exclude_categories=["FURNISHED_FLAT"], anotherParam="test")
    print(json.dumps(rent_listings, indent=2))

    # Search for additional rental properties
    additional_rent_listings = client.search_rent_listings(rent_categories, 10000)
    print(json.dumps(additional_rent_listings, indent=2))
