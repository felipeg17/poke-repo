import pytest
from pokemon.pokemon import Pokemon

def test_bulbasaur_no_evolves_before_16():
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=15)
    assert bulba.can_evolve() is False

def test_bulbasaur_evolves_at_16_to_ivysaur():
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=16)
    assert bulba.can_evolve() is True
    assert bulba.evolve() is True
    assert bulba.get_attribute("pokemon_name") == "ivysaur"

def test_nidorina_evolves_with_moon_stone():
    nidorina = Pokemon("nidorina", 30, "poison", "blue", "female", level=25)
    assert nidorina.can_evolve(item="Moon Stone") is True
    assert nidorina.evolve(item="Moon Stone") is True
    assert nidorina.get_attribute("pokemon_name") == "nidoqueen"