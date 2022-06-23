import os
import pathlib

import yaml


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_fp = os.path.join(parent_dir, "docker-compose.yml")
    with open(dc_fp) as f:
        dc = yaml.safe_load(f)
    service_keys = list(dc["services"].keys())
    service = dc["services"][service_keys[0]]
    assert service["image"].startswith("neo4j:")
    assert len(service["environment"]) >= 1
    assert len(service["ports"]) >= 2

