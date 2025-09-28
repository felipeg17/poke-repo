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
    assert stats.sp_attack == stats.base_sp_attack
    assert stats.sp_defense == stats.base_sp_defense
    assert stats.speed == stats.base_speed
    bulbasaur.level_up()

    stats = bulbasaur.stats()

    assert stats.hp > stats.base_hp, "HP should increase after the pokemon levels up"
    assert stats.attack > stats.base_attack, "Attack should increase after the pokemon levels up"
    assert stats.defense > stats.base_defense, "Defense should increase after the pokemon levels up"
    assert stats.sp_attack > stats.base_sp_attack, "Special Attack should increase after the pokemon levels up"
    assert stats.sp_defense > stats.base_sp_defense, "Special Defense should increase after the pokemon levels up"
    assert stats.speed > stats.base_speed, "Speed should increase after the pokemon levels up"

    stats = charmander.stats()  

    assert stats.hp == stats.base_hp 
    assert stats.attack == stats.base_attack
    assert stats.defense == stats.base_defense
    assert stats.sp_attack == stats.base_sp_attack
    assert stats.sp_defense == stats.base_sp_defense
    assert stats.speed == stats.base_speed

    charmander.level_up()

    stats = charmander.stats()

    assert stats.hp > stats.base_hp, "HP should increase after the pokemon levels up"
    assert stats.attack > stats.base_attack, "Attack should increase after the pokemon levels up"
    assert stats.defense > stats.base_defense, "Defense should increase after the pokemon levels up"
    assert stats.sp_attack > stats.base_sp_attack, "Special Attack should increase after the pokemon levels up"
    assert stats.sp_defense > stats.base_sp_defense, "Special Defense should increase after the pokemon levels up"
    assert stats.speed > stats.base_speed, "Speed should increase after the pokemon levels up"


if __name__ == "__main__":
    test_create_pokemon()
    test_pokemon_resistances()
    # test_pokemon_stats()
# if __name__ == "__main__":
#     test_create_pokemon()
#     test_pokemon_resistances()

