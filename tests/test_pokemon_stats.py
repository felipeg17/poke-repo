from pokemon import Pokemon


def test_pokemon_stats_base():
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        type="grass",
        level=1,
        pokedex_num=1,
        color="green",
        sex="male",
    )

    stats = bulbasaur.get_stats()
    assert stats.hp == stats.base_hp
    assert stats.attack == stats.base_attack
    assert stats.defense == stats.base_defense
    assert stats.sp_attack == stats.base_sp_attack
    assert stats.sp_defense == stats.base_sp_defense
    assert stats.speed == stats.base_speed


def test_pokemon_stats_level_increase():
    lvl10_bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        type="grass",
        level=10,
        pokedex_num=1,
        color="green",
        sex="male",
    )

    lvl10_stats = lvl10_bulbasaur.get_stats()

    assert round(lvl10_stats.hp) == 63
    assert round(lvl10_stats.attack) == 58
    assert round(lvl10_stats.defense) == 58
    assert round(lvl10_stats.sp_attack) == 74
    assert round(lvl10_stats.sp_defense) == 74
    assert round(lvl10_stats.speed) == 46


def test_level_up_method_increases_stats():
    charmander = Pokemon(
        pokemon_name="charmander",
        type="fire",
        level=5,
        pokedex_num=4,
        color="red",
        sex="male",
    )
    charmander.level_up()
    stats_after = charmander.get_stats()

    assert charmander.get_attribute("level") == 6
    assert round(stats_after.hp) == 44
    assert round(stats_after.attack) == 57
    assert round(stats_after.defense) == 43
    assert round(stats_after.sp_attack) == 65
    assert round(stats_after.sp_defense) == 55
    assert round(stats_after.speed) == 70
