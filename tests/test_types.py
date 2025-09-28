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
def test_pokemon_stats():
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

    stats = bulbasaur.stats() 

    assert stats.hp == stats.base_hp 
    assert stats.attack == stats.base_attack
    assert stats.defense == stats.base_defense
    assert stats.spattack == stats.base_spattack
    assert stats.spdefense == stats.base_spdefense
    assert stats.speed == stats.base_speed
    bulbasaur.level_up()

    stats = bulbasaur.stats()

    assert stats.hp > stats.base_hp, "HP should increase after the pokemon levels up"
    assert stats.attack > stats.base_attack, "Attack should increase after the pokemon levels up"
    assert stats.defense > stats.base_defense, "Defense should increase after the pokemon levels up"
    assert stats.spattack > stats.base_spattack, "Special Attack should increase after the pokemon levels up"
    assert stats.spdefense > stats.base_spdefense, "Special Defense should increase after the pokemon levels up"
    assert stats.speed > stats.base_speed, "Speed should increase after the pokemon levels up"

    stats = charmander.stats()  

    assert stats.hp == stats.base_hp 
    assert stats.attack == stats.base_attack
    assert stats.defense == stats.base_defense
    assert stats.spattack == stats.base_spattack
    assert stats.spdefense == stats.base_spdefense
    assert stats.speed == stats.base_speed

    charmander.level_up()

    stats = charmander.stats()

    assert stats.hp > stats.base_hp, "HP should increase after the pokemon levels up"
    assert stats.attack > stats.base_attack, "Attack should increase after the pokemon levels up"
    assert stats.defense > stats.base_defense, "Defense should increase after the pokemon levels up"
    assert stats.spattack > stats.base_spattack, "Special Attack should increase after the pokemon levels up"
    assert stats.spdefense > stats.base_spdefense, "Special Defense should increase after the pokemon levels up"
    assert stats.speed > stats.base_speed, "Speed should increase after the pokemon levels up"


if __name__ == "__main__":
    test_create_pokemon()
    test_pokemon_resistances()
    test_pokemon_stats()

