from homegater.utils import _is_valid_geo_tag, convert_to_camel_case


def test_convert_to_camel_case_simple():
    snake_case_dict = {"first_name": "John", "last_name": "Doe"}
    expected_result = {"firstName": "John", "lastName": "Doe"}
    assert convert_to_camel_case(snake_case_dict) == expected_result


def test_convert_to_camel_case_nested():
    snake_case_dict = {"user_info": {"first_name": "John", "last_name": "Doe"}}
    expected_result = {"userInfo": {"first_name": "John", "last_name": "Doe"}}
    assert convert_to_camel_case(snake_case_dict) == expected_result


def test_convert_to_camel_case_empty():
    snake_case_dict = {}
    expected_result = {}
    assert convert_to_camel_case(snake_case_dict) == expected_result


def test_convert_to_camel_case_mixed_keys():
    snake_case_dict = {
        "first_name": "John",
        "lastName": "Dalton",
        "age": 30,
        "is_active": True,
    }
    expected_result = {
        "firstName": "John",
        "lastName": "Dalton",
        "age": 30,
        "isActive": True,
    }
    assert convert_to_camel_case(snake_case_dict) == expected_result


def test_geo_tag():
    test_geo = [
        ("geo-canton-zurich", True),
        ("geo-region-horgen", True),
        ("geo-zipcode-8800", True),
        ("geo-gemeinde-thalwil", False),
        ("xyz", False),
        ("xyx-xyx-xyz", False),
    ]
    for location, expected in test_geo:
        assert _is_valid_geo_tag(location) == expected
