import json

from airflow.hooks.sqlite_hook import SqliteHook
from dags import long_track


def test_get_quote(responses):
    with open('tests/data/comments.json', 'r') as file:
        comments = json.load(file)

    responses.add(responses.GET,
                  long_track.COMMENTS_API_ROOT,
                  json=comments)
    last_comments = long_track.get_last_comments()
    assert len(responses.calls) == 1
    assert last_comments == comments['comments']


def test_double_single_quote():
    comment_with_single_quote = "Don't waste your time and money on it."
    assert long_track.double_single_quote(comment_with_single_quote) == "Don''t waste your time and money on it."


def test_load_to_database():
    with open('tests/data/comments.json', 'r') as file:
        comments = json.load(file)

    hook = SqliteHook(sqlite_conn_id='sqlite_connection')
    hook.run(sql="""DROP TABLE IF EXISTS comments;""")
    hook.run(sql="""CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                comment VARCHAR NOT NULL,
                rating INTEGER NOT NULL
            );""")
    connection = hook.get_conn()
    cursor = connection.cursor()
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 0
    long_track.load_to_database(comments['comments'], hook)
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 3
    inserted_comments = cursor.execute("SELECT * FROM comments;").fetchall()
    assert inserted_comments[0] == (1, 1, 'Comment 1 of movie 1', 4)
    assert inserted_comments[1] == (2, 1, 'Comment 2 of movie 1', 3)
    assert inserted_comments[2] == (3, 2, 'Comment 1 of movie 2', 3)
    long_track.load_to_database(comments['comments'], hook)
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 6


def test_get_and_insert_last_comments(responses):
    with open('tests/data/comments.json', 'r') as file:
        comments = json.load(file)

    responses.add(responses.GET,
                  long_track.COMMENTS_API_ROOT,
                  json=comments)

    hook = SqliteHook(sqlite_conn_id='sqlite_connection')
    hook.run(sql="""DROP TABLE IF EXISTS comments;""")
    hook.run(sql="""CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                comment VARCHAR NOT NULL,
                rating INTEGER NOT NULL
            );""")
    connection = hook.get_conn()
    cursor = connection.cursor()
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 0

    long_track.get_and_insert_last_comments(hook)

    assert len(responses.calls) == 1
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 3
    inserted_comments = cursor.execute("SELECT * FROM comments;").fetchall()
    assert inserted_comments[0] == (1, 1, 'Comment 1 of movie 1', 4)
    assert inserted_comments[1] == (2, 1, 'Comment 2 of movie 1', 3)
    assert inserted_comments[2] == (3, 2, 'Comment 1 of movie 2', 3)
    long_track.load_to_database(comments['comments'], hook)
    assert cursor.execute("SELECT COUNT(*) FROM comments;").fetchall()[0][0] == 6
