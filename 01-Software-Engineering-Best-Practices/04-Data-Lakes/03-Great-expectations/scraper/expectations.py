import great_expectations as gx
import pandas as pd
import requests
import os


def send_message(message: str):
    """
    Sends a message to the Wagon Chat channel.

    This function posts a message to the Wagon Chat channel specified by the environment variable `LAKE_BUCKET`.
    The message is sent with the author name "ge".

    Parameters:
    ----------
    message : str
        The content of the message to be sent to the chat channel.

    Returns:
    -------
    None

    Raises:
    ------
    HTTPError:
        If the post request to the chat channel fails.
    """
    base_url = "https://wagon-chat.herokuapp.com"
    channel = os.environ["LAKE_BUCKET"]
    url = f"{base_url}/{channel}/messages"

    data = dict(author="ge", content=message)
    response = requests.post(url, data=data)
    response.raise_for_status()


def run_expectations(df: pd.DataFrame):
    """
    Validates a given DataFrame against a predefined set of expectations using Great Expectations.

    The function performs the following steps:
    1. Gets the current Great Expectations context.
    2. Adds or updates a pandas datasource.
    3. Adds a dataframe asset to the datasource.
    4. Builds a batch request using the provided DataFrame.
    5. Creates or updates a checkpoint for validation.
    6. Runs the checkpoint and captures the result.
    7. Builds data documentation.
    8. Iterates through the validation results to check for failures.
    9. Sends appropriate messages based on the validation outcome.

    Parameters:
    ----------
    df : pd.DataFrame
        The pandas DataFrame to be validated.

    Returns:
    -------
    None
    """
    context = gx.get_context()

    datasource = context.sources.add_or_update_pandas(name="hn_df")
    data_asset = datasource.add_dataframe_asset(name="hn_df")
    batch_request = data_asset.build_batch_request(dataframe=df)
    checkpoint = context.add_or_update_checkpoint(
        name="check_hn",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "hn_expectation_suite"
            }
        ],
    )
    checkpoint_result = checkpoint.run()
    context.build_data_docs()
    #print()

    failures = []
    for expectation_result in checkpoint_result.list_validation_results():
        if not expectation_result["success"]:
            failures.append(expectation_result)

    if failures:
        for failure in failures:
            send_message("Expectation failed!")
            send_message("site")
    else:
        send_message("All expectations passed!")
