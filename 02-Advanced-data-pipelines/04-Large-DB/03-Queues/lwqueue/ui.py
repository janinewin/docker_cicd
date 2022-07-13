from rich.live import Live
from rich.table import Table 

from lwqueue import message

from typing import List


def make_rich_table(messages_old_to_recent: List[message.Message]) -> Table:
    table = Table()
    table.add_column("Username")
    table.add_column("Date / time")
    table.add_column("Message")

    for message in reversed(messages_old_to_recent):
        table.add_row(message["username"], message["received_at"], message["message"])

    return table
