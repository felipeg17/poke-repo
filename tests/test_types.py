import pytest

from pokemon import (
    Pokemon, Grass, Fire
    )

def test_create_pokemon():
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        type="Grass",
        level=5,
        pokedex_num=1,
        color="green",
        sex="male"
    )
    assert bulbasaur.get_attribute("pokemon_name") == "bulbasaur"
    assert bulbasaur.get_attribute("type") == "Grass"
    assert bulbasaur.get_attribute("level") == 5
    assert bulbasaur.get_attribute("pokedex_num") == 1
    assert bulbasaur.get_attribute("color") == "green"
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

def test_pokemon_stats():
    bulbasaur = Grass(
        name="bulbasaur",
        level=1,
        pokedex_num=1,
        color="green",
        sex="male"
    )

    stats = bulbasaur.get_stats() 
    assert stats.hp == stats.base_hp 
    assert stats.attack == stats.base_attack
    assert stats.defense == stats.base_defense
    assert stats.sp_attack == stats.base_sp_attack
    assert stats.sp_defense == stats.base_sp_defense
    assert stats.speed == stats.base_speed

def test_evolutions():
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=15)
    assert bulba.can_evolve() is False

    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=16)
    assert bulba.can_evolve() is True
    assert bulba.evolve() is True
    assert bulba.get_attribute("pokemon_name") == "ivysaur"

    nidorina = Pokemon("nidorina", 30, "poison", "blue", "female", level=25)
    assert nidorina.can_evolve(item="Moon Stone") is True
    assert nidorina.evolve(item="Moon Stone") is True
    assert nidorina.get_attribute("pokemon_name") == "nidoqueen"


if __name__ == "__main__":
    test_create_pokemon()
    test_pokemon_resistances()
    test_pokemon_stats()
    test_evolutions()

