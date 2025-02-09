import json

from homegater.client import FLAT_CATEGORY, HOUSE_CATEGORY, Homegate

client = Homegate(location_search_lang="en")

star = 80 * "*"

# Example: Search with different location and fewer parameters
kwargs = {
    "lotSize": {"from": 100, "to": 3000},
    "livingSpace": {"from": 50, "to": 400},
    "numberOfRooms": {"from": 3, "to": 6},
    "yearBuilt": {"from": 2010, "to": 2025},
    "hasBalcony": True,
    "purchasePrice": {"from": 200000, "to": 3000000},
}

buy_listings = client.search_buy_listings(
    categories=HOUSE_CATEGORY, location="Geneva", **kwargs
)
print(json.dumps(buy_listings, indent=2))
print(star)

# Example: Search with minimal parameters using the post code
kwargs = {"purchasePrice": {"from": 500000, "to": 2000000}}

buy_listings = client.search_buy_listings(
    categories=HOUSE_CATEGORY, location=["8050", "8820", "Horgen"], **kwargs
)
print(json.dumps(buy_listings, indent=2))
print(star)

# Get a specific listing
listing_id = 4001544515
listing_details = client.get_listing(listing_id)
print(json.dumps(listing_details, indent=2))
print(star)

# Example: Search for properties to rent with an extra parameter (monthly rent)
kwargs = {"monthlyRent": {"from": 100, "to": 3000000}}

rent_listings = client.search_rent_listings(
    categories=FLAT_CATEGORY,
    location="Thalwil",
    exclude_categories=["FURNISHED_FLAT"],
    monthly_rent="test",
)
print(json.dumps(rent_listings, indent=2))
print(star)

# Example: Search for properties with now parameters in German

# location search lanuage is german
client = Homegate(location_search_lang="de")

additional_rent_listings = client.search_rent_listings()
print(json.dumps(additional_rent_listings, indent=2))
print(star)


kwargs = {
    "lotSize": {"from": 50, "to": 5000},
    "livingSpace": {"from": 20, "to": 500},
    "numberOfRooms": {"from": 4.5, "to": 8},
    "yearBuilt": {"from": 2005, "to": 2025},
    "purchasePrice": {"from": 100000, "to": 4000000},
    "cubage": {"from": 6, "to": 55555},
    # "hasBalcony": False,
    # "hasElevator": False,
    # "isWheelchairAccessible": False,
    # "isNewBuilding": False,
    # "hasSwimmingPool": False,
    # "isOldBuilding": False,
    # "isMinergie": False,
    # "hasParkingOrGarage": True,
    # "isPriceDefined": True,
}


buy_listings = client.search_buy_listings(
    categories=HOUSE_CATEGORY, location="Kanton Zürich", **kwargs
)
print(json.dumps(buy_listings, indent=2))
