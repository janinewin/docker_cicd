# Import FastAPI
# IMPORT YOUR PACKAGES HERE

# Import datetime
# IMPORT YOUR PACKAGES HERE

from lwapi import rural


# Create an `app` variable with a FastAPI API
# YOUR CODE HERE

# YOUR CODE HERE
def time():
    # Replace `dt = None` with the current time
    dt = None
    pass  # YOUR CODE HERE
    return {
        "h": dt.hour,
        "m": dt.minute,
        "s": dt.second
    }


# YOUR CODE HERE
def rural_population_percentage(country: str, year: int):
    dataset = rural.load_rural_csv()
    # Fill the `value` of the rural population percentage for the right country and year
    value = 0
    pass  # YOUR CODE HERE
    return value
