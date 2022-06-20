import lewagonde


def test_genres_original_schema():
    sql = "select count(*) from movies_metadata where genres ~ 'Drama';"
