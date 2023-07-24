from pokemon.lookup import (
    get_pokemon,
    check_pokemon_move,
    get_pokemon_types,
    get_evolutions,
)
import ast
from pathlib import Path


def test_import_requests():
    file_path = Path(__file__).parent.parent / "pokemon" / "lookup.py"
    target_library = "requests"

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    imports = [node for node in tree.body if isinstance(node, ast.Import)]
    import_names = [alias.name for imp in imports for alias in imp.names]

    assert (
        target_library in import_names
    ), f"The library '{target_library}' was not imported in the file."


def test_get_pokemon():
    assert (
        1281 <= get_pokemon()["count"]
    ), "Should return all of the pokemon. The count is too low"
    assert 1 == len(
        get_pokemon(limit=1)["results"]
    ), "Should return only one pokemon when limit is set to 1"
    assert (
        "ivysaur" == get_pokemon(limit=1, offset=1)["results"][0]["name"]
    ), "Second pokemon should be 'ivysaur'"
    expected = [
        {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
    ]
    assert (
        expected == get_pokemon(limit=2, offset=1)["results"]
    ), "Should return 'ivysaur' and 'venusaur' when limit is set to 2 and offset to 1"


def test_check_pokemon_move():
    assert (
        True is check_pokemon_move()
    ), "Default pokemon 'bulbasaur' be able to learn move 'swords-dance'"
    assert False is check_pokemon_move(
        name="bulbasaur", move="fake-move"
    ), "Pokemon 'bulbasaur' should not be able to learn move 'fake-move'"
    assert True is check_pokemon_move(
        name="charmeleon", move="mega-punch"
    ), "Pokemon 'charmeleon' should be able to learn 'mega-punch'"


def test_get_pokemon_types():
    assert 99 <= len(
        get_pokemon_types(type_one="fighting")
    ), "Should return all fighting type pokemon. The count is too low"
    assert ["crabominable"] == get_pokemon_types(
        type_one="fighting", type_two="ice"
    ), "Only 'crabominable' is both 'fighting' and 'ice' type"
    assert [] == get_pokemon_types(
        type_one="dragon", type_two="bug"
    ), "No pokemon should be both 'dragon' and 'bug' type"


def test_get_evolutions():
    assert {"from": "charmeleon"} == get_evolutions(
        "charizard"
    ), "Charizard evolves from Charmeleon"
    assert {"from": "charmander", "to": ["charizard"]} == get_evolutions(
        "charmeleon"
    ), "Charmeleon evolves from Charmander and evolves to Charizard"
    assert {} == get_evolutions(
        "mew"
    ), "Mew does not evolve from or to any other Pokemon"
    assert {"from": "oddish", "to": ["vileplume", "bellossom"]} == get_evolutions(
        "gloom"
    ), "Gloom evolves from Oddish and can evolve to either Vileplume or Bellossom"
