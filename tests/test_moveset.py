import pytest
from pokemon import Pokemon
from pokemon.moveset import Moveset

def test_pokemon_moveset_initialization():
    # Checks that a Pokemon's moveset is initialized correctly (no more than 4 moves)

    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        pokedex_num=1,
        type="Grass",
        color="green",
        sex="male",
        level=25
    )

    moveset = bulbasaur._moveset  
    assert moveset is not None, "The pokemon should have a moveset"
    assert len(moveset.current_moves) <= 4, "The moveset should have at most 4 moves"

def test_pokemon_moveset_has_expected_moves():
    # Verifies that the moveset contains expected move names for a given Pokemon and level in the CSV data

    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        pokedex_num=1,
        type="Grass",
        color="green",
        sex="male",
        level=50
    )

    moveset = bulbasaur._moveset
    move_names = moveset.get_moves_names()

    assert isinstance(move_names, list), "The move names should be returned as a list"
    assert all(isinstance(name, str) for name in move_names), "Each move name should be a string"
    assert len(move_names) <= 4, "The moveset should have at most 4 moves"

def test_show_moves_output(capsys):
    # Tests that show_moves prints the correct output format

    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        pokedex_num=1,
        type="Grass",
        color="green",
        sex="male",
        level=50
    )

    bulbasaur.show_moves()
    captured = capsys.readouterr() # Capture printed output
    output = captured.out.strip() # Get the standard output

    # Check that output is not empty and has expected format
    assert len(output) > 0, "It should print some moves"
    assert "-" in output, "The output should list moves with '-' prefix"

def test_pokemon_without_moves(monkeypatch):
    # Tests behavior when a Pokemon has no learnable moves

    def mock_load_available_moves(self):
        return []  # No moves available

    # Force the Moveset to use the mock method
    monkeypatch.setattr(Moveset, "_load_available_moves", mock_load_available_moves)

    pokemon = Pokemon(
        pokemon_name="missingno",
        pokedex_num=1,   
        type="Normal",
        color="gray",
        sex="none",
        level=1
    )

    moveset = pokemon._moveset
    assert len(moveset.current_moves) == 0, "Pokemon with no learnable moves should have an empty moveset"
