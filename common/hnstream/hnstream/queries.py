from typing import List, Tuple

from google.cloud import bigquery

DEFAULT_LIMIT = 100


def table_metadata(table: str) -> Tuple[str, List[bigquery.ScalarQueryParameter]]:
    """
    Returns the query and parameters to get metadata about a table
    """
    assert table in ["stories", "comments"]
    query = """
    SELECT * EXCEPT(is_generated, generation_expression, is_stored, is_updatable)
    FROM `bigquery-public-data.hacker_news`.INFORMATION_SCHEMA.COLUMNS
    WHERE table_name = @table
    """
    query_parameters = [bigquery.ScalarQueryParameter("table", "STRING", table)]

    return query, query_parameters


def all_after(table: str, unix_time: int, limit: int = DEFAULT_LIMIT):
    """
    Get the next `limit` stories after a given `unix_time`
    """
    assert table in ["stories", "comments"]
    limit = DEFAULT_LIMIT if limit == 0 else min(100, max(1, int(limit)))
    query = f"""
    SELECT * FROM `bigquery-public-data.hacker_news`.stories
    WHERE time >= @time
    LIMIT {limit}
    """
    query_parameters = [bigquery.ScalarQueryParameter("time", "INT64", unix_time)]

    return query, query_parameters


def stories_after(unix_time: int, limit: int = DEFAULT_LIMIT):
    """
    `all_after` on stories
    """
    return all_after(table="stories", unix_time=unix_time, limit=limit)


def comments_after(unix_time: int, limit: int = DEFAULT_LIMIT):
    """
    `all_after` on comments
    """
    return all_after(table="comments", unix_time=unix_time, limit=limit)
