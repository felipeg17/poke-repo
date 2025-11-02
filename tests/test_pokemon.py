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
    
def test_pokemon_resistances_and_weaknesses():
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
    assert bulbasaur.receive_attack("Electric") == "It's not very effective..."
    assert charmander.receive_attack("Normal") == "It's effective."

def test_pokemon_stats_base():
    bulbasaur = Grass(
        name="bulbasaur",
        level=1,
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

def test_pokemon_stats_level_increase():
    base_bulbasaur = Grass(
        name="bulbasaur",
        level=1,
        pokedex_num=1,
        color="green",
        sex="male"
    )
    lvl10_bulbasaur = Grass(
        name="bulbasaur",
        level=10,
        pokedex_num=1,
        color="green",
        sex="male"
    )

    base_stats = base_bulbasaur.get_stats()
    lvl10_stats = lvl10_bulbasaur.get_stats()

    assert round(lvl10_stats.hp) == 63
    assert round(lvl10_stats.attack) == 58
    assert round(lvl10_stats.defense) == 58
    assert round(lvl10_stats.sp_attack) == 74
    assert round(lvl10_stats.sp_defense) == 74
    assert round(lvl10_stats.speed) == 46

def test_level_up_method_increases_stats():
    charmander = Fire(
        name="charmander",
        level=5,
        pokedex_num=4,
        color="red",
        sex="male"
    )
    stats_before = charmander.get_stats()
    charmander.level_up()
    stats_after = charmander.get_stats()

    assert charmander.get_attribute("level") == 6
    assert round(stats_after.hp) == 44
    assert round(stats_after.attack) == 57
    assert round(stats_after.defense) == 43
    assert round(stats_after.sp_attack) == 65
    assert round(stats_after.sp_defense) == 55
    assert round(stats_after.speed) == 70

if __name__ == "__main__":
    pass

