import pytest
from pokemon.pokemon import Pokemon

def test_bulbasaur_evolves_at_level_16():
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=16)
    assert bulba.can_evolve() is True
    assert bulba.evolve() is True

def test_nidorina_evolves_with_moon_stone():
    nido = Pokemon("nidorina", 30, "poison", "blue", "female", level=30)
    assert nido.can_evolve(item="Moon Stone") is True
    assert nido.evolve(item="Moon Stone") is True

def test_bulbasaur_does_not_evolve_before_level_16():
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=15)
    assert bulba.can_evolve() is False
    assert bulba.evolve() is False 
    