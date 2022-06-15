import pytest
from yaml import load
from yaml.loader import SafeLoader

class TestTask1:
    
    @pytest.fixture
    def docker_validation(self):
        return load("""
        version: '3.9'
        services:
            webapi:
                container_name: fastapi
                build:
                    context: .
                    dockerfile: dockerfile-fastapi
                restart: on-failure
                ports:
                    - "8000:8000"
                volumes:
                    - ./app-no-database:/server/app
                command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        """
        , SafeLoader)
    
    @pytest.mark.skip(reason="Too strict")  
    def test_docker_compose_strict(self, docker_validation):
        with open('docker-compose-1.yml') as f:
            docker_compose_data = load(f, SafeLoader)
            assert docker_validation == docker_compose_data


    def test_docker_compose(self, docker_validation):
        keys_to_check = [
            'webapi',
            'container_name',
            'build',
            'context',
            'dockerfile',
            'restart',
            'ports',
            'volumes'
        ]

        def get_keys(d, keys=None):
            keys = keys or []  
            if isinstance(d, dict):
                keys += d.keys()
                _ = [get_keys(x, keys) for x in d.values()]
            elif isinstance(d, list):
                _ = [get_keys(x, keys) for x in d]
            return list(set(keys))

        with open('docker-compose-1.yml') as f:
            docker_compose_data = load(f, SafeLoader)
            
            keys = get_keys(docker_compose_data)
            assert all(item in keys for item in keys_to_check)
            