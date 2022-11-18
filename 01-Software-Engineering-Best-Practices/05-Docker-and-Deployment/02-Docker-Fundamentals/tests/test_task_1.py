import dockerfile
import pytest


class TestTask1:
    @pytest.fixture
    def dockerfile_validation(self):
        return {
            "FROM": "ubuntu:20.04",
            "ARG": "DEBIAN_FRONTEND=noninteractive",
            "ENV": "PYTHONUNBUFFERED 1",
            "RUN": [
                "apt-get -y update",
                "apt-get -y upgrade",
                "apt-get -y install software-properties-common",
                "add-apt-repository ppa:deadsnakes/ppa",
                "apt-get -y update",
                "apt-get -y install python3.8 python3-pip",
                "pip3 install fastapi==0.78.0 SQLAlchemy==1.4.36 alembic==1.7.7 uvicorn[standard]==0.17.6",
                "apt-get clean",
                "rm -rf /var/lib/apt/lists/*",
            ],
            "WORKDIR": "/server",
            "COPY": "./ ./",
            "EXPOSE": "8000",
            "ENTRYPOINT": "uvicorn",
            "CMD": "app.main:app --host 0.0.0.0 --port 8000",
        }

    @pytest.mark.skip(reason="Can be too rigid - check your solution visually against tests/test_task_1.py")
    def test_dockerfile_task_1_strict(self, dockerfile_validation):
        dockerfile_name = "dockerfile-task-1"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in dockerfile_validation
            # if we have the same instructions repeated in the dockerfile, value is stored as a list:
            if isinstance(dockerfile_validation.get(command.cmd), list):
                assert " ".join(command.value) in dockerfile_validation.get(command.cmd)
            else:
                assert " ".join(command.value) == dockerfile_validation.get(command.cmd)

    def test_dockerfile_task_1_keys_only(self):
        dockerfile_name = "dockerfile-task-1"
        dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

        keys_to_check = ["FROM", "ARG", "ENV", "RUN", "WORKDIR", "COPY", "EXPOSE", "ENTRYPOINT", "CMD"]
        for command in dockerfile_parsed:
            # Checks key is present in dictionnary
            assert command.cmd in keys_to_check
