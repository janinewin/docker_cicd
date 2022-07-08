import os

import yaml


def test_profiles_yml():
    assert "profiles.yml" in os.listdir("lewagon_dbt")
    with open("lewagon_dbt/profiles.yml", "r") as stream:
        profiles = yaml.safe_load(stream)
        assert "lewagon_dbt" in profiles
        assert "outputs" in profiles["lewagon_dbt"]
        assert "dev" in profiles["lewagon_dbt"]["outputs"]
        dev = profiles["lewagon_dbt"]["outputs"]["dev"]
        assert set(dev.keys()) == {
            "dataset",
            "job_execution_timeout_seconds",
            "job_retries",
            "location",
            "method",
            "priority",
            "project",
            "threads",
            "type",
            "keyfile",
        }
        assert dev["dataset"].startswith("dbt_")
        assert dev["dataset"].endswith("day2")
        assert dev["job_execution_timeout_seconds"] == 300
        assert dev["job_retries"] == 1
        assert dev["location"] == "US"
        assert dev["method"] == "service-account"
        assert dev["priority"] == "interactive"
        assert dev["project"] is not None
        assert dev["threads"] == 1
        assert dev["type"] == "bigquery"
        assert dev["keyfile"].startswith("/opt/airflow/.gcp_keys/")
        assert dev["keyfile"].endswith(".json")
