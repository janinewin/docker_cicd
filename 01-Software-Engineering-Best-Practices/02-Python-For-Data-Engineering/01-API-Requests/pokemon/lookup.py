
# Make sure to add the correct imports here
from typing import Optional, Union, List
import requests

def get_pokemon(limit: int = 100, offset: int = 0) -> dict:
    """Get a list of pokemon. Return a dictionary containing the results. Limit the results to `limit` and offset by `offset`"""
    params = {"limit": limit, "offset": offset}
    response = requests.get("https://pokeapi.co/api/v2/pokemon/", params=params)
    response_json = response.json()
    return response_json


def check_pokemon_move(name: str = "bulbasaur", move: str = "swords-dance") -> bool:
    """Check if a pokemon can learn a move. Return True if it can, False otherwise."""
    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+name).json()
    for move_i in response["moves"]:
        if move_i["move"]["name"] == move: return True
    return False


def get_pokemon_types(
    type_one: str = "flying", type_two: Optional[Union[None, str]] = None
) -> List[Optional[str]]:
    """
    Get all pokemon of a given type `type_one`. Return a list of pokemon names.
    If `type_two` is given return only the Pokemon of type_one and type_two.
    """
    result = []
    response_t_one = requests.get("https://pokeapi.co/api/v2/type/"+type_one).json()
    for pk in response_t_one["pokemon"]: result.append(pk["pokemon"]["name"])

    if type_two != None:
        response_t_two = requests.get("https://pokeapi.co/api/v2/type/"+type_two).json()
        tmp = []
        for pk in response_t_two["pokemon"]:
            if pk["pokemon"]["name"] in result: tmp.append(pk["pokemon"]["name"])
        result = tmp

    return result


def get_evolutions(name: str) -> dict:
    """
    For a given pokemon return a dictionary containing the pokemon it evolves
    from and into. The structure should be:
    {"from": "pokemon_name", "to": ["pokemon_name"]}
    If the pokemon does not evolve from or into another pokemon
    do not include the relevant key.
    """
    result = {}
    response = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+name).json()
    if response["evolves_from_species"]: result["from"] = response["evolves_from_species"]["name"]

    ev_chain = requests.get(response["evolution_chain"]["url"]).json()
    branch = ev_chain["chain"]
    to_not_found = True
    while to_not_found:
        if branch["species"]["name"] == name:
            evols = []
            for e in branch["evolves_to"]:
                evols.append(e["species"]["name"])
            if len(evols) > 0: result["to"] = evols
            to_not_found = False
        else: branch = branch["evolves_to"][0]
    return result
