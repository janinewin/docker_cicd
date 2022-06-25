import os
import pathlib
import json

from lewagonde import docker_compose
import yaml


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_fp = os.path.join(parent_dir, "docker-compose.yml")
    with open(dc_fp) as f:
        dc = yaml.safe_load(f)

    volumes = dc["services"]["postgres"]["volumes"]
    expected_volumes = ["./data/database/:/var/lib/postgresql/data", "./data/files:/files"]
    assert list(sorted(volumes)) == list(sorted(expected_volumes)), "Wrong volumes"

    environment = docker_compose.dict_or_kvlist_to_dict(dc["services"]["postgres"]["environment"])
    assert environment == {"POSTGRES_DB": "db", "POSTGRES_PASSWORD": "$POSTGRES_PASSWORD", "POSTGRES_USER": "lewagon"}, "Wrong Docker compose"
