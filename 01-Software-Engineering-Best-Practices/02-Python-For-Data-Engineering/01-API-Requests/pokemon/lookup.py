
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
    params = {"limit": 5, "offset": 0}
    result = []
    response = requests.get("https://pokeapi.co/api/v2/pokemon/", params = params).json()
    #print(response)

    #next = True
    #while next:
    pokemon = response["results"]
    for poke in pokemon:
        p = requests.get(poke["url"]).json()
        types = []
        print(p["types"]["type"])
    #    for type in p["types"]:
    #        types.append(type["type"]["name"])
    #    if (type_two == None and type_one in types) or (type_two != None and type_one in types and type_two in types):
    #        result.append(p["name"])
    #    if response["next"] == None: next = False
    #    response = requests.get(response["next"]).json()


    #for poke in pokemon:
    #    print(poke["types"])
        #for type in poke["types"]:
        #    print(type)
    return result


def get_evolutions(name: str) -> dict:
    """
    For a given pokemon return a dictionary containing the pokemon it evolves
    from and into. The structure should be:
    {"from": "pokemon_name", "to": ["pokemon_name"]}
    If the pokemon does not evolve from or into another pokemon
    do not include the relevant key.
    """
    pass  # YOUR CODE HERE

print(get_pokemon_types())
