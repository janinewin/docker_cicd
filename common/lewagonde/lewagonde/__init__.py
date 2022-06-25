__version__ = "0.1.0"

from lewagonde.pandas import read_sql_query
from lewagonde.comp import soft_equal
from lewagonde.docker_compose import docker_compose_equal, dict_or_kvlist_to_dict
from lewagonde.env import load_dot_env

__all__ = [
    "read_sql_query",
    "soft_equal",
    "docker_compose_equal",
    "load_dot_env",
    "dict_or_kvlist_to_dict"
]
