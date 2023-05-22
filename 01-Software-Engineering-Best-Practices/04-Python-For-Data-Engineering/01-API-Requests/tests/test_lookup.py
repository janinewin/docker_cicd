from pokemon.lookup import (
    get_pokemon,
    check_pokemon_move,
    get_pokemon_types,
    get_evolutions,
)


def test_get_pokemon():
    assert 1000 <= get_pokemon()["count"]
    assert 1 == len(get_pokemon(limit=1)["results"])
    assert "ivysaur" == get_pokemon(limit=1, offset=1)["results"][0]["name"]
    expected = [
        {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
    ]
    assert expected == get_pokemon(limit=2, offset=1)["results"]


def test_check_pokemon_move():
    assert True is check_pokemon_move()
    assert False is check_pokemon_move(name="bulbasaur", move="fake-move")
    assert True is check_pokemon_move(name="charmeleon", move="mega-punch")


def test_get_pokemon_types():
    assert 99 <= len(get_pokemon_types(type_one="fighting"))
    assert ["crabominable"] == get_pokemon_types(type_one="fighting", type_two="ice")
    assert [] == get_pokemon_types(type_one="dragon", type_two="bug")


def test_get_evolutions():
    assert {"from": "charmeleon"} == get_evolutions("charizard")
    assert {"from": "charmander", "to": ["charizard"]} == get_evolutions("charmeleon")
    assert {} == get_evolutions("mew")
    assert {"from": "oddish", "to": ["vileplume", "bellossom"]} == get_evolutions(
        "gloom"
    )
