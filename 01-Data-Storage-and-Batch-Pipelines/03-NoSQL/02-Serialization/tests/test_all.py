import os


def test_there_is_a_csv_file():
    from lwserialization import rural
    assert os.path.isfile(rural.get_rural_csv_fp()), "file API-rural.csv not found under data/"


def test_import_pandas():
    from lwserialization import rural
    vars = dir(rural)
    assert "pandas" in vars, "pandas can't be found in lwserialization/rural"


def test_load_file():
    from lwserialization import rural
    import pandas
    assert type(rural.load_rural_csv()) == type(pandas.DataFrame([])), "the loaded file isn't a pandas.DataFrame"


def test_columns():
    from lwserialization import rural
    assert rural.explore_columns() == 67, "wrong number of columns"


def test_size():
    from lwserialization import rural
    assert rural.explore_size() == 266, "wrong dataset size"


def test_countries():
    from lwserialization import rural
    assert rural.explore_countries() == 266, "wrong number of countries"


def test_to_parquet():
    from lwserialization import rural
    df = rural.load_rural_csv()
    fp = "/tmp/pq.parquet"
    rural.dataframe_to_parquet(df, fp)


def test_parquetted():
    from lwserialization import rural
    assert os.path.isfile(rural.get_rural_csv_fp().replace(".csv", ".parquet")), "data/API-rural.parquet is not found"
