def city_name_validator(city_name):
    """The city_name must contain just letters.

    Args:
        city_name (string): Replace the upper case letters to lower case letters
        Replace the empty spaces between the words to math with isalpha method.

    Returns:
        boolean: True if all the characters are alphabet letters
    """
    city_name = city_name.lower()
    city_name = city_name.replace(" ", "")
    return city_name.isalpha()

def max_number_validator(max_number):
    """The max_number must be numeric.

    Args:
        max_number (parameter - string): parameter from a route

    Returns:
        boolean: True if the requirement match with the condition.
    """
    if max_number.isnumeric():
        max_number = int(max_number)
        if max_number > 0:
            is_numeric = True
        else:
            is_numeric = False
    else:
        is_numeric = False

    return is_numeric