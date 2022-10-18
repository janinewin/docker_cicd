import os
import pathlib
import json

import lewagonde
import yaml


def test_docker_compose_setup():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_fp = os.path.join(parent_dir, "docker-compose.yml")
    with open(dc_fp) as f:
        dc = yaml.safe_load(f)

    volumes = dc["services"]["postgres"]["volumes"]
    expected_volumes = ["./data/database/:/var/lib/postgresql/data", "./data/files:/files"]
    assert list(sorted(volumes)) == list(sorted(expected_volumes)), "Wrong postgres volumes"

    environment = lewagonde.dict_or_kvlist_to_dict(dc["services"]["postgres"]["environment"])
    assert environment == {"POSTGRES_DB": "db", "POSTGRES_PASSWORD": "$POSTGRES_PASSWORD", "POSTGRES_USER": "lewagon"}, "Wrong setup of postgres credentials"

    postgres_ports_mapping = dc["services"]["postgres"]["ports"]
    assert postgres_ports_mapping == ["5432:5432"], "Postgres ports not mapped correctly"

    adminer_ports_mapping = dc["services"]["adminer"]["ports"]
    assert adminer_ports_mapping == ["8080:8080"], "Adminer ports not mapped correctly"
