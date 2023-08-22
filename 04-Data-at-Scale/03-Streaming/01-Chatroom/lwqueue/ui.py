from rich.table import Table

from lwqueue import message

from typing import List


def make_rich_table(messages_old_to_recent: List[message.Message]) -> Table:
    """
    Generate a new Rich table with headers and 3 columns
    Add all messages to the table, from most recent to oldest
    """
    table = Table()
    table.add_column("Username", justify="left", style="green")
    table.add_column("Date / time", style="magenta")
    table.add_column("Message", justify="right", style="cyan", no_wrap=True)

    # This will allow us to get messages from the most recent to the oldest
    messages_recent_to_old = reversed(messages_old_to_recent)

    pass  # YOUR CODE HERE

    return table
