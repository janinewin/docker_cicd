import json

from airflow.hooks.sqlite_hook import SqliteHook
from dags import track_long


def test_get_last_comments(responses):
    with open('tests/data/comments.json', 'r') as file:
        comments = json.load(file)

    responses.add(responses.GET,
                  f"{track_long.COMMENTS_API_ROOT}?n=3",
                  json=comments)
    last_comments = track_long.get_last_comments(3)
    assert len(responses.calls) == 1
    assert last_comments == comments['comments']


def test_double_single_quote():
    comment_with_single_quote = "Don't waste your time and money on it."
    assert track_long.double_single_quote(comment_with_single_quote) == "Don''t waste your time and money on it."


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
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 0

    track_long.load_to_database(comments['comments'], hook)
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 3
    inserted_comments = hook.get_records("SELECT * FROM comments;")
    assert inserted_comments[0] == (1, 1, 'Comment 1 of movie 1', 4)
    assert inserted_comments[1] == (2, 1, 'Comment 2 of movie 1', 3)
    assert inserted_comments[2] == (3, 2, 'Comment 1 of movie 2', 3)
    track_long.load_to_database(comments['comments'], hook)
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 6


def test_get_and_insert_last_comments(responses):
    with open('tests/data/comments.json', 'r') as file:
        comments = json.load(file)
    comments['comments'].append({'movie_id': 2, 'comment': "Comment 2 of movie 2 with a single quote '", 'rating': 1})
    comments['comments'].append({'movie_id': 2, 'comment': 'Comment 3 of movie 2', 'rating': 5})

    responses.add(responses.GET,
                  f"{track_long.COMMENTS_API_ROOT}?n=5",
                  json=comments)

    hook = SqliteHook(sqlite_conn_id='sqlite_connection')
    hook.run(sql="""DROP TABLE IF EXISTS comments;""")
    hook.run(sql="""CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                comment VARCHAR NOT NULL,
                rating INTEGER NOT NULL
            );""")
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 0

    track_long.get_and_insert_last_comments(hook)
    assert len(responses.calls) == 1
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 5
    inserted_comments = hook.get_records("SELECT * FROM comments;")
    assert inserted_comments[0] == (1, 1, 'Comment 1 of movie 1', 4)
    assert inserted_comments[1] == (2, 1, 'Comment 2 of movie 1', 3)
    assert inserted_comments[2] == (3, 2, 'Comment 1 of movie 2', 3)
    assert inserted_comments[3] == (4, 2, "Comment 2 of movie 2 with a single quote '", 1)
    assert inserted_comments[4] == (5, 2, 'Comment 3 of movie 2', 5)
    track_long.load_to_database(comments['comments'], hook)
    assert hook.get_records("SELECT COUNT(*) FROM comments;")[0][0] == 10
