import argparse
import random
import time

from rich.live import Live
from rich.table import Table


def generate_table() -> Table:
    """
    Make a new table.
    """
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS")
    return table


def make_callback(live: Live):
    """
    Return a function to be called on a new RabbitMQ message
    Will call live.update()
    """
    pass


def main():
    with Live(generate_table(), refresh_per_second=1) as live:
        # Start RabbitMQ connection / subscription etc.
        callback = make_callback(live)

        # Here for demo purposes first
        for _ in range(40):
            time.sleep(0.4)
            live.update(generate_table())


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == "__main__":
    _args = parse_args()
    main()
