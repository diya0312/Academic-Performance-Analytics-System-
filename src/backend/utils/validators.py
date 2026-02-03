def is_valid_string(value):
    return isinstance(value, str) and value.strip() != ""

def is_valid_number(value):
    try:
        float(value)
        return True
    except:
        return False
