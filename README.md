# Homegater

This is a client python api aim to query homegate.ch buy and rent properties. The python package and client API is done purely for academic/experimental purpose and not approved for any commercial usage. It is not an official API.


# Installation

To get the latest version just

```
pip install homegater
```

# Usage


```python

from homegater import Homegate

api = Homegate()

# Search by zip-code
api.search_rent_listings(location="8001")

# Search by Gemeinde
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

```

More examples can be found on [API usage examples](./examples/api_usage.py).

## Location

The location should be a valid location used in homegate.ch search. The suggested and most straight forward/robust way is to provide the zip codes. If the location cannot be uniquely determined an exception will be raised.