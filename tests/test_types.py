import pytest

from pokemon import (
    Pokemon, Grass, Fire
    )

def test_create_pokemon():
    bulbasaur = Pokemon(
        name="bulbasaur",
        type="Grass",
        level=5,
        pokedex_num=1,
        color="green",
        sex="male"
    )
    print(bulbasaur)
    assert bulbasaur.name == "bulbasaur"
    assert bulbasaur.pokedex_num == 1
    assert bulbasaur.main_type == "Grass"
    assert bulbasaur.attack() == "bulbasaur is attacking!"
    

def test_pokemon_resistances():
    bulbasaur = Grass(
        name="bulbasaur",
        level=5,
        pokedex_num=1,
        color="green",
        sex="male"
    )
    charmander = Fire(
        name="charmander",
        level=5,
        pokedex_num=4,
        color="red",
        sex="male"
    )
    assert bulbasaur.receive_attack("Fire") == "It's super effective!"
    assert bulbasaur.receive_attack("Water") == "It's not very effective..."
    assert charmander.receive_attack("Water") == "It's super effective!"
    assert charmander.receive_attack("Grass") == "It's not very effective..."

# if __name__ == "__main__":
#     test_create_pokemon()
#     test_pokemon_resistances()

