from homegater.utils import convert_to_camel_case


def test_convert_to_camel_case_simple():
    snake_case_dict = {
        "first_name": "John",
        "last_name": "Doe"
    }
    expected_result = {
        "firstName": "John",
        "lastName": "Doe"
    }
    assert convert_to_camel_case(snake_case_dict) == expected_result

def test_convert_to_camel_case_nested():
    snake_case_dict = {
        "user_info": {
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    expected_result = {
        "userInfo": {
            "first_name": "John",
            "last_name": "Doe"
        }
    }
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
        "is_active": True
    }
    expected_result = {
        "firstName": "John",
        "lastName": "Dalton",
        "age": 30,
        "isActive": True
    }
    assert convert_to_camel_case(snake_case_dict) == expected_result
