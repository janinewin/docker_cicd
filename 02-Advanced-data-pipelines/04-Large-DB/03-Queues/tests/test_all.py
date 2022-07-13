import os
import pathlib

import lewagonde


def test_docker_compose():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dc_path = os.path.join(parent_dir, "docker-compose.yml")

    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent
    dc_correction_path = os.path.join(parent_dir, "_x", "docker-compose.correction.yml")

    lewagonde.docker_compose_equal(dc_path, dc_correction_path)
