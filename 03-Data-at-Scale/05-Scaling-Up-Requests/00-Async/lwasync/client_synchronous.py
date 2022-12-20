from typing  import Any, Dict, List
import time

# The library to make synchronous HTTP requests
import requests

from lwasync import argument_parser


def make_one_call() -> Dict[str, Any]:
    """
    Make one call to the API
    """
    response = None
    # Replace `None` by a call to the API, using the `requests` library
    # YOUR CODE HERE
    return response


def make_many_calls(n: int) -> List[Dict[str, Any]]:
    """
    Runs n synchronous calls to the local server and returns all the responses in an array
    """
    t0 = time.time()

    responses = []
    # Below write synchronous code with the `requests` library, and append them to the `responses` array
    # YOUR CODE HERE

    tf = time.time()
    print(f"It took {tf-t0} seconds to run the {n} synchronous calls!")
    return responses


def main():
    """
    The main function to run this file as a standalone program
    """
    # First we get the command line arguments, check
    args = argument_parser.parse_args()
    # Then we call the function `make_many_calls` with the argument `number` of the `args` object
    make_many_calls(args.number)


if __name__ == "__main__":
    # Here we simply call `main()` when this file is run as a program and not imported as a library
    main()
