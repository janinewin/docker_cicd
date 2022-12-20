# Import FastAPI
# IMPORT YOUR PACKAGES HERE

# Import datetime
# IMPORT YOUR PACKAGES HERE

from src import rural


# Create an `app` variable with a FastAPI API
# YOUR CODE HERE

# YOUR CODE HERE
def time():
    """Get the current time using the datetime module.
    Use the hour, minute and second attributes of the datetime object.

    Returns:
        str: The current time in the format HH,MM,SS
    """

    # Replace `dt = None` with the current time
    dt = None
    pass  # YOUR CODE HERE


# YOUR CODE HERE
def rural_population_percentage(country: str, year: int):
    dataset = rural.load_rural_csv()
    # Fill the `value` of the rural population percentage for the right country and year
    value = 0
    pass  # YOUR CODE HERE
    return value
