from pathlib import Path

import pandas as pd
import pytest

fixtures_dir = Path(__file__).resolve().parent / "fixtures"

@pytest.fixture
def top_drivers_dataFrame():
    return pd.read_csv(fixtures_dir / "top_drivers.csv")
