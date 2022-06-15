import pytest
from pathlib import Path
import pandas as pd


fixtures_dir = Path(__file__).resolve().parent / 'fixtures'

@pytest.fixture
def race_id():
    return 1009

@pytest.fixture
def race_name_for_id_1009():
    return 'Abu Dhabi Grand Prix'

@pytest.fixture
def races_dataFrame():
    return pd.read_csv( fixtures_dir / 'races_2018.csv')

@pytest.fixture
def lap_times_for_race_989_dataFrame():
    return pd.read_csv( fixtures_dir / 'lap_times_989.csv')

@pytest.fixture
def best_lap_times_for_race_989_dataFrame():
    return pd.read_csv( fixtures_dir / 'best_lap_times_989.csv')

@pytest.fixture
def fastest_lap_for_race_989():
    return pd.read_csv( fixtures_dir / 'fastest_lap_989.csv')