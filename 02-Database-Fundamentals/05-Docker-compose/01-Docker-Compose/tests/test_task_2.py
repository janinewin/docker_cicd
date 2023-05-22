from yaml import load
from yaml.loader import SafeLoader


class TestTask2:
    def test_docker_compose(self):
        keys_to_check = [
            "webapi",
            "container_name",
            "restart",
            "ports",
            "volumes",
            "networks",
        ]

        def get_keys(d, keys=None):
            keys = keys or []
            if isinstance(d, dict):
                keys += d.keys()
                _ = [get_keys(x, keys) for x in d.values()]
            elif isinstance(d, list):
                _ = [get_keys(x, keys) for x in d]
            return list(set(keys))

        with open("docker-compose-2.yml") as f:
            docker_compose_data = load(f, SafeLoader)

            keys = get_keys(docker_compose_data)
            for item in keys_to_check:
                assert (
                    item in keys
                ), f"Expected {item} element in the docker-compose file"
