# Homegater

This is a client python api aim to query homegate.ch buy and rent properties. The python package and client API is done purely for academic/experimental purpose and not approved for any commercial usage. It is not an official API.


# Installation

If you want to ge the latest version


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
api.search_buy_listings(location="Horgen")

# Search in Switzerland
api.search_buy_listings()

# Specify arguments
kwargs = {"monthlyRent": {"from": 100, "to": 3000000}}
api.search_rent_listings(location="8001", **kwargs)

```

More examples can be found on [API usage examples](./examples/api_usage.py).

## Location

The location should be a valid location used in homegate.ch search. The suggested and most straight forward/robust is to provide the zip codes.


## Further Improvements

Make the location searching more robust even when the user provides the location name.