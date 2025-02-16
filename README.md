# Homegater

This is a client python api aim to query homegate.ch buy and rent properties. The python package and client API is done purely for academic/experimental purpose and not approved for any usage (e.g. it is **prohibited** to systematically read out the content made available on the marketplaces -e.g. by scraping, copy it, publish it or otherwise reproduce it in any form (e.g. on the Internet), or to link it to other data.). It is **not** an official API. See further https://www.homegate.ch/c/de/ueber-uns/rechtliches/agb.


## Installation

To get the latest version just

```
pip install homegater
```

## Usage


```python

from homegater import Homegate

api = Homegate()

# Search by zip-code
api.search_rent_listings(location="8001")

# Search by Gemeinde/city
api.search_buy_listings(location="Thalwil")

# Search in geo
api.search_buy_listings(location="geo-canton-zurich")
api.search_buy_listings(location="geo-city-richterswil")

# Search multiple
api.search_buy_listings(location=["geo-canton-zurich", "8810"])


# Search in Switzerland
api.search_buy_listings()


# Specify arguments
kwargs = {"monthlyRent": {"from": 100, "to": 3000000}}
api.search_rent_listings(location="8001", **kwargs)

# Pagination
api.search_buy_listings(location="geo-canton-zurich", from_index=30, size=10)

```

The location should be a valid location used in homegate.ch search. The suggested and most straight forward/robust way is to provide the zip codes. If the location cannot be uniquely determined an exception will be raised.

More examples can be found on [API usage examples](./examples/api_usage.py).

## Location

Homegate search api uses a `geo-tag` to search for advertisements. `geo-tag` is a string that starts with "geo" and can take the following forms:

- canton: e.g. `"geo-canton-zurich"`
- city: e.g. `"geo-city-richterswil"`
- region e.g. `"geo-region-horgen"`
- country e.g. `"geo-country-switzerland"`
- zipcode e.g. `"geo-zipcode-8810"`
  
The client method 

```python
api.get_geo_tag(location)

e.g. 

api.get_geo_tag("richterswil")

```

can retrieve the geo tag for a given location by querying the endpoint `https://api.homegate.ch/geo/locations`. The endpoint will return the relevant geo-tags which can be more than one. By querying Horgen for example (`https://api.homegate.ch/geo/locations?lang=en&name=Horgen&size=100`) the response includes (`geo-city-horgen, geo-region-horgen, geo-city-horgenberg, geo-zipcode-8815, geo-zipcode-8810`). To avoid any confusion, the `search_(buy_rent)_listings` functionalities of the api, will raise an exceptions if the location cannot be uniquely determined.

## Contributing

We welcome pull requests 