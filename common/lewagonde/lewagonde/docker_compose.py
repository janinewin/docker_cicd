from typing import Any, Dict, List

import json
import yaml

from lewagonde.comp import soft_equal


def is_key_value_like(txt: str) -> bool:
    """
    Checks if `txt` is of the form <something>=<some other thing>
    """

    lr = txt.split("=")
    return len(lr) == 2 and lr[0] != "" and lr[1] != ""


def is_kvlist(l: List[str]) -> bool:
    """
    Returns true iff the list is only made of strings of the sort `<some key>=<some value>`
    """
    for row in l:
        if not isinstance(row, str) or not is_key_value_like(row):
            return False
    return True


def kvlist_to_dict(kvlist: List[str]) -> Dict[str, str]:
    """
    Turns `["A=10", "B=20"]` to `{"A": 10, "B": 20}`
    """
    return dict([kv.split("=") for kv in kvlist])


def dict_or_kvlist_to_dict(d):
    """
    Applies kvlist_to_dict to key-value lists, or returns the input dict
    """
    if is_kvlist(d):
        return kvlist_to_dict(d)
    elif isinstance(d, dict):
        return d
    else:
        raise ValueError("Not a kvlist or a dict")


def docker_compose_transform_dict_block(dc_dict_block: Dict[str, Any]):
    """
    - Recursively transforms dictionaries into sorted strings
    - Removes single and double quotes
    """
    sorted_keys = sorted(dc_dict_block.keys())
    lines = []
    for key in sorted_keys:
        value_obj = dc_dict_block[key]
        value_str = ""
        if isinstance(value_obj, dict):
            # Dict -> docker_compose_transform_dict_block -> json.dumps
            value_str = docker_compose_transform_dict_block(value_obj)
        elif isinstance(value_obj, list) and is_kvlist(value_obj):
            # KVList -> Dict -> docker_compose_transform_dict_block -> json.dumps
            value_str = docker_compose_transform_dict_block(kvlist_to_dict(value_obj))
        else:
            # Anything else -> json.dumps
            value_str = json.dumps(value_obj)

        lines.append(f"{key}:{value_str}")
    return "".join(lines).replace("\"", "").replace("'", "")


def docker_compose_equal(dc1_fp: str, dc2_fp: str):
    """
    Checks if two Docker-Compose files are equal.
    - Recursively transforms dictionaries into sorted strings
    - Checks soft equality between the strings
    """
    with open(dc1_fp) as f:
        dc1 = yaml.safe_load(f)
    with open(dc2_fp) as f:
        dc2 = yaml.safe_load(f)
    return docker_compose_equal_content(dc1, dc2)


def docker_compose_equal_content(dc1: Dict[str, Any], dc2: Dict[str, Any]):
    """
    Checks parsed Docker-Compose YAML soft equality
    """
    tr_dc1 = docker_compose_transform_dict_block(dc1)
    tr_dc2 = docker_compose_transform_dict_block(dc2)

    return soft_equal(tr_dc1, tr_dc2)
