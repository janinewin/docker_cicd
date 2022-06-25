import os


def load_dot_env(dot_env_fp: str = "./.env"):
    """
    Given a `dot_env_fp`, parse it and export all of the env vars
    """
    envs = []
    with open(dot_env_fp) as f:
        for line in f:
            if line.startswith("#"):
                continue
            split = line.split("=")
            if len(split) != 2:
                continue
            envs.append((split[0], split[1]))

    for k, v in envs:
        os.environ[k] = v
