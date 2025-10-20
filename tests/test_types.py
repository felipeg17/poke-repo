import pytest
from pokemon import Pokemon, Grass, Fire, Water

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

    assert lvl10_stats.hp > base_stats.hp
    assert lvl10_stats.attack > base_stats.attack
    assert lvl10_stats.defense > base_stats.defense
    assert lvl10_stats.sp_attack > base_stats.sp_attack
    assert lvl10_stats.sp_defense > base_stats.sp_defense
    assert lvl10_stats.speed > base_stats.speed

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
    assert stats_after.hp >= stats_before.hp
    assert stats_after.attack >= stats_before.attack
    assert stats_after.defense >= stats_before.defense
    assert stats_after.sp_attack >= stats_before.sp_attack
    assert stats_after.sp_defense >= stats_before.sp_defense
    assert stats_after.speed >= stats_before.speed


if __name__ == "__main__":
    test_create_pokemon()
    test_pokemon_resistances()
    test_pokemon_stats()


