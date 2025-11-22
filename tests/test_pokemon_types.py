from pokemon import Pokemon


def test_create_pokemon():
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        type="grass",
        level=5,
        pokedex_num=1,
        color="green",
        sex="male",
    )
    assert bulbasaur.get_attribute("pokemon_name") == "bulbasaur"
    assert bulbasaur.get_attribute("type") == "grass"
    assert bulbasaur.get_attribute("level") == 5
    assert bulbasaur.get_attribute("pokedex_num") == 1
    assert bulbasaur.get_attribute("color") == "green"
    assert bulbasaur.attack() == "bulbasaur is attacking!"


def test_pokemon_resistances_and_weaknesses():
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        type="grass",
        level=5, 
        pokedex_num=1,
        color="green",
        sex="male"
    )
    charmander = Pokemon(
        pokemon_name="charmander",
        type="fire",
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
