def require_type(value, expected_type, value_name, location=None, details=None):
    if not isinstance(value, expected_type):
        location_str = f" ({location})" if location else ""
        detail_str = f" {details}." if details else ""
        raise ValueError(
            f"Missing or invalid '{value_name}'{location_str}. "
            f"Required type: {expected_type.__name__}."
            f"{detail_str}"
        )

def optional_type(value, expected_type, value_name, location=None, details=None):
    if value is None:
        return
    require_type(value, expected_type, value_name, location, details)

def require_in_set(value, valid_set, value_name, location=None, details=None):
    if value not in valid_set:
        location_str = f" ({location})" if location else ""
        detail_str = f" {details}." if details else ""
        valid_str = ", ".join(f"'{x}'" for x in sorted(valid_set))
        raise ValueError(
            f"Invalid '{value_name}'{location_str}. "
            f"Valid values are: {valid_str}."
            f"{detail_str}"
        )

def require_non_empty_list(value, value_name, location=None, details=None):
    require_type(value, list, value_name, location, details)
    if not value:
        location_str = f" ({location})" if location else ""
        detail_str = f" {details}." if details else ""
        raise ValueError(
            f"Missing or invalid '{value_name}'{location_str}. "
            f"Required non-empty list."
            f"{detail_str}"
        )

def require_list_of_type(value, expected_type, value_name, location=None, details=None):
    require_type(value, list, value_name, location, details)
    if not all(isinstance(x, expected_type) for x in value):
        location_str = f" ({location})" if location else ""
        detail_str = f" {details}." if details else ""
        raise ValueError(
            f"Invalid '{value_name}'{location_str}. "
            f"Required type: list of {expected_type.__name__}."
            f"{detail_str}"
        )

def require_int_in_range(value, value_name, location=None, details=None, min_value=None, max_value=None):
    require_type(value, int, value_name, location, details)
    if (
        (min_value is not None and value < min_value) 
        or 
        (max_value is not None and value > max_value)
    ):
        location_str = f" ({location})" if location else ""
        detail_str = f" {details}." if details else ""
        min_str = "-∞" if min_value is None else str(min_value)
        max_str = "+∞" if max_value is None else str(max_value)
        raise ValueError(
            f"Invalid '{value_name}'{location_str}. "
            f"Required range: [{min_str}, {max_str}]."
            f"{detail_str}"
        )

def optional_int_in_range(value, value_name, location=None, details=None, min_value=None, max_value=None):
    if value is None:
        return
    require_int_in_range(value, value_name, location, details, min_value, max_value)

def require_asset_exists(asset_path, location):
    if not asset_path.is_file():
        location_str = f" ({location})" if location else ""
        raise ValueError(f"File not found: '{asset_path}'{location_str}.")