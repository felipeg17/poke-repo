import pytest
from pokemon.pokemon import Pokemon

# ============= Level Evolution Tests =============

def test_bulbasaur_evolves_at_level_16():
    """Test that Bulbasaur can evolve at exactly level 16"""
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=16)
    assert bulba.can_evolve() is True
    assert bulba.evolve() is True

def test_bulbasaur_does_not_evolve_before_level_16():
    """Test that Bulbasaur cannot evolve before level 16"""
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=15)
    assert bulba.can_evolve() is False
    assert bulba.evolve() is False

def test_bulbasaur_evolves_above_level_16():
    """Test that Bulbasaur can still evolve well above level 16"""
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=25)
    assert bulba.can_evolve() is True
    assert bulba.evolve() is True

def test_ivysaur_evolves_at_level_32():
    """Test second stage evolution (Ivysaur to Venusaur)"""
    ivy = Pokemon("ivysaur", 2, "grass", "blue", "male", level=32)
    assert ivy.can_evolve() is True
    assert ivy.evolve() is True

def test_caterpie_evolves_at_level_7():
    """Test early evolution (Caterpie at level 7)"""
    caterpie = Pokemon("caterpie", 10, "bug", "green", "male", level=7)
    assert caterpie.can_evolve() is True
    assert caterpie.evolve() is True

def test_metapod_evolves_at_level_10():
    """Test Metapod evolution at level 10"""
    metapod = Pokemon("metapod", 11, "bug", "green", "male", level=10)
    assert metapod.can_evolve() is True
    assert metapod.evolve() is True

def test_dragonair_evolves_at_level_55():
    """Test late evolution (Dragonair at level 55)"""
    dragonair = Pokemon("dragonair", 148, "dragon", "blue", "male", level=55)
    assert dragonair.can_evolve() is True
    assert dragonair.evolve() is True

# ============= Stone Evolution Tests =============

def test_pikachu_evolves_with_thunder_stone():
    """Test Pikachu evolution with Thunder Stone"""
    pikachu = Pokemon("pikachu", 25, "electric", "yellow", "male", level=1)
    assert pikachu.can_evolve(item="Thunder Stone") is True
    assert pikachu.evolve(item="Thunder Stone") is True

def test_pikachu_does_not_evolve_by_level():
    """Test that Pikachu doesn't evolve by level (only stone)"""
    pikachu = Pokemon("pikachu", 25, "electric", "yellow", "male", level=50)
    assert pikachu.can_evolve() is False
    assert pikachu.evolve() is False

def test_clefairy_evolves_with_moon_stone():
    """Test Clefairy evolution with Moon Stone"""
    clefairy = Pokemon("clefairy", 35, "fairy", "pink", "female", level=20)
    assert clefairy.can_evolve(item="Moon Stone") is True
    assert clefairy.evolve(item="Moon Stone") is True

def test_nidorina_evolves_with_moon_stone():
    """Test Nidorina evolution with Moon Stone"""
    nido = Pokemon("nidorina", 30, "poison", "blue", "female", level=30)
    assert nido.can_evolve(item="Moon Stone") is True
    assert nido.evolve(item="Moon Stone") is True

def test_eevee_evolves_with_stone():
    """Test Eevee evolution with any stone"""
    eevee = Pokemon("eevee", 133, "normal", "brown", "male", level=10)
    assert eevee.can_evolve(item="Water Stone") is True
    assert eevee.evolve(item="Fire Stone") is True

def test_vulpix_evolves_with_fire_stone():
    """Test Vulpix evolution with Fire Stone"""
    vulpix = Pokemon("vulpix", 37, "fire", "brown", "female", level=15)
    assert vulpix.can_evolve(item="Fire Stone") is True
    assert vulpix.evolve(item="Fire Stone") is True

def test_gloom_evolves_with_leaf_stone():
    """Test Gloom can evolve with Leaf Stone (also has level requirement)"""
    gloom = Pokemon("gloom", 44, "grass", "blue", "female", level=30)
    assert gloom.can_evolve(item="Leaf Stone") is True
    assert gloom.evolve(item="Leaf Stone") is True

def test_stone_evolution_without_item():
    """Test that stone evolution Pokemon don't evolve without item"""
    pikachu = Pokemon("pikachu", 25, "electric", "yellow", "male", level=30)
    assert pikachu.can_evolve() is False
    assert pikachu.evolve() is False

# ============= Trade Evolution Tests =============

def test_kadabra_evolves_by_trade():
    """Test Kadabra evolution by trade"""
    kadabra = Pokemon("kadabra", 64, "psychic", "yellow", "male", level=16)
    assert kadabra.can_evolve(trade=True) is True
    assert kadabra.evolve(trade=True) is True

def test_kadabra_evolves_by_trade_string():
    """Test Kadabra evolution using 'trade' as item string"""
    kadabra = Pokemon("kadabra", 64, "psychic", "yellow", "male", level=20)
    assert kadabra.can_evolve(item="trade") is True
    assert kadabra.evolve(item="Trade") is True

def test_machoke_evolves_by_trade():
    """Test Machoke evolution by trade"""
    machoke = Pokemon("machoke", 67, "fighting", "gray", "male", level=35)
    assert machoke.can_evolve(trade=True) is True
    assert machoke.evolve(trade=True) is True

def test_haunter_evolves_by_trade():
    """Test Haunter evolution by trade"""
    haunter = Pokemon("haunter", 93, "ghost", "purple", "male", level=30)
    assert haunter.can_evolve(trade=True) is True
    assert haunter.evolve(trade=True) is True

def test_graveler_evolves_by_trade():
    """Test Graveler evolution by trade"""
    graveler = Pokemon("graveler", 75, "rock", "gray", "male", level=40)
    assert graveler.can_evolve(trade=True) is True
    assert graveler.evolve(trade=True) is True

def test_trade_evolution_without_trade():
    """Test that trade evolution Pokemon don't evolve without trade (below level threshold)"""
    kadabra = Pokemon("kadabra", 64, "psychic", "yellow", "male", level=20)
    assert kadabra.can_evolve() is False
    assert kadabra.evolve() is False

# ============= No Evolution Tests =============

def test_venusaur_does_not_evolve():
    """Test final evolution Pokemon (Venusaur) cannot evolve"""
    venusaur = Pokemon("venusaur", 3, "grass", "green", "male", level=100)
    assert venusaur.can_evolve() is False
    assert venusaur.evolve() is False

def test_charizard_does_not_evolve():
    """Test final evolution Pokemon (Charizard) cannot evolve"""
    charizard = Pokemon("charizard", 6, "fire", "orange", "male", level=80)
    assert charizard.can_evolve() is False
    assert charizard.evolve() is False

def test_legendary_does_not_evolve():
    """Test legendary Pokemon (Mewtwo) cannot evolve"""
    mewtwo = Pokemon("mewtwo", 150, "psychic", "purple", "genderless", level=70)
    assert mewtwo.can_evolve() is False
    assert mewtwo.evolve() is False
    assert mewtwo.can_evolve(item="Moon Stone") is False
    assert mewtwo.can_evolve(trade=True) is False

def test_snorlax_does_not_evolve():
    """Test single-stage Pokemon (Snorlax) cannot evolve"""
    snorlax = Pokemon("snorlax", 143, "normal", "blue", "male", level=50)
    assert snorlax.can_evolve() is False
    assert snorlax.evolve() is False

def test_chansey_does_not_evolve():
    """Test single-stage Pokemon (Chansey) cannot evolve"""
    chansey = Pokemon("chansey", 113, "normal", "pink", "female", level=40)
    assert chansey.can_evolve() is False
    assert chansey.evolve() is False

# ============= Evolution Hint Tests =============

def test_evolution_hint_level():
    """Test evolution hint for level-based evolution"""
    bulbasaur = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=10)
    hint = bulbasaur.evolution_hint()
    assert "nivel 16" in hint.lower() or "level 16" in hint.lower()

def test_evolution_hint_stone():
    """Test evolution hint for stone-based evolution"""
    pikachu = Pokemon("pikachu", 25, "electric", "yellow", "male", level=15)
    hint = pikachu.evolution_hint()
    assert "piedra" in hint.lower() or "stone" in hint.lower()

def test_evolution_hint_trade():
    """Test evolution hint for trade-based evolution"""
    kadabra = Pokemon("kadabra", 64, "psychic", "yellow", "male", level=20)
    hint = kadabra.evolution_hint()
    assert "intercambio" in hint.lower() or "trade" in hint.lower()

def test_evolution_hint_no_evolution():
    """Test evolution hint for non-evolving Pokemon"""
    mewtwo = Pokemon("mewtwo", 150, "psychic", "purple", "genderless", level=70)
    hint = mewtwo.evolution_hint()
    assert "no evoluciona" in hint.lower() or "does not evolve" in hint.lower()

# ============= Evolution Transformation Tests =============

def test_bulbasaur_transforms_to_ivysaur():
    """Test that Bulbasaur actually transforms into Ivysaur with updated stats"""
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=16)
    
    # Get original stats
    original_name = bulba.get_attribute("pokemon_name")
    original_pokedex = bulba.get_attribute("pokedex_num")
    original_stats = bulba.get_stats()
    original_hp = original_stats.hp
    
    # Evolve
    assert bulba.evolve() is True
    
    # Check transformation
    assert bulba.get_attribute("pokemon_name") == "ivysaur"
    assert bulba.get_attribute("pokedex_num") == 2
    assert bulba.get_attribute("level") == 16  # Level should stay the same
    
    # Check stats increased (Ivysaur has higher base stats than Bulbasaur)
    new_stats = bulba.get_stats()
    assert new_stats.base_hp > original_stats.base_hp  # Ivysaur: 60 vs Bulbasaur: 45
    assert new_stats.hp > original_hp  # Current HP should also be higher

def test_evolution_stats_scale_with_level():
    """Test that evolved Pokemon stats are properly scaled to current level"""
    # Bulbasaur at level 20
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=20)
    
    # Evolve to Ivysaur
    assert bulba.evolve() is True
    
    # Stats should be Ivysaur's base stats + level 20 scaling
    stats = bulba.get_stats()
    
    # Ivysaur base stats: HP=60, Attack=62, Defense=63, Sp.Atk=80, Sp.Def=80, Speed=60
    # At level 20, stats should be higher than base stats
    assert stats.base_hp == 60
    assert stats.base_attack == 62
    assert stats.base_defense == 63
    assert stats.base_sp_attack == 80
    assert stats.base_sp_defense == 80
    assert stats.base_speed == 60
    
    # Current stats should be scaled for level 20
    assert stats.hp > stats.base_hp
    assert stats.attack > stats.base_attack

def test_charmander_evolution_chain():
    """Test full evolution chain: Charmander -> Charmeleon -> Charizard"""
    # Start with Charmander at level 16
    charmander = Pokemon("charmander", 4, "fire", "orange", "male", level=16)
    original_stats = charmander.get_stats()
    
    # Evolve to Charmeleon
    assert charmander.evolve() is True
    assert charmander.get_attribute("pokemon_name") == "charmeleon"
    assert charmander.get_attribute("pokedex_num") == 5
    charmeleon_stats = charmander.get_stats()
    assert charmeleon_stats.base_hp > original_stats.base_hp
    
    # Level up to 36
    for _ in range(20):  # 16 + 20 = 36
        charmander.level_up()
    
    assert charmander.get_attribute("level") == 36
    
    # Evolve to Charizard
    assert charmander.can_evolve() is True
    assert charmander.evolve() is True
    assert charmander.get_attribute("pokemon_name") == "charizard"
    assert charmander.get_attribute("pokedex_num") == 6
    charizard_stats = charmander.get_stats()
    assert charizard_stats.base_hp > charmeleon_stats.base_hp

def test_pikachu_stone_evolution_stats():
    """Test that stone evolution properly updates stats"""
    pikachu = Pokemon("pikachu", 25, "electric", "yellow", "male", level=30)
    pikachu_stats = pikachu.get_stats()
    
    # Pikachu base: HP=35, Attack=55
    assert pikachu_stats.base_hp == 35
    assert pikachu_stats.base_attack == 55
    
    # Evolve with Thunder Stone
    assert pikachu.evolve(item="Thunder Stone") is True
    
    # Check it became Raichu
    assert pikachu.get_attribute("pokemon_name") == "raichu"
    assert pikachu.get_attribute("pokedex_num") == 26
    
    # Raichu has higher base stats: HP=60, Attack=90
    raichu_stats = pikachu.get_stats()
    assert raichu_stats.base_hp == 60
    assert raichu_stats.base_attack == 90
    
    # Current stats at level 30 should be much higher
    assert raichu_stats.hp > pikachu_stats.hp
    assert raichu_stats.attack > pikachu_stats.attack

def test_evolution_preserves_level():
    """Test that evolution doesn't change the Pokemon's level"""
    caterpie = Pokemon("caterpie", 10, "bug", "green", "male", level=7)
    
    assert caterpie.get_attribute("level") == 7
    assert caterpie.evolve() is True
    assert caterpie.get_attribute("level") == 7  # Should still be level 7
    
    # But name and pokedex should change
    assert caterpie.get_attribute("pokemon_name") == "metapod"
    assert caterpie.get_attribute("pokedex_num") == 11

def test_high_level_evolution_stats():
    """Test evolution at high level has properly scaled stats"""
    # Dratini at level 50
    dratini = Pokemon("dratini", 147, "dragon", "blue", "male", level=50)
    
    # Evolve to Dragonair (level 30 requirement, but Pokemon is level 50)
    assert dratini.evolve() is True
    assert dratini.get_attribute("pokemon_name") == "dragonair"
    
    # Stats should be scaled for level 50
    stats = dratini.get_stats()
    # Dragonair base: HP=61, but at level 50 it should be much higher
    assert stats.base_hp == 61
    assert stats.hp > 100  # At level 50, HP should be significantly boosted

def test_cannot_evolve_again_at_final_form():
    """Test that Pokemon cannot evolve once at final evolution"""
    bulba = Pokemon("bulbasaur", 1, "grass", "blue", "male", level=32)
    
    # Evolve to Ivysaur
    assert bulba.evolve() is True
    assert bulba.get_attribute("pokemon_name") == "ivysaur"
    
    # Evolve to Venusaur
    assert bulba.evolve() is True
    assert bulba.get_attribute("pokemon_name") == "venusaur"
    
    # Try to evolve again - should fail
    assert bulba.can_evolve() is False
    assert bulba.evolve() is False
    assert bulba.get_attribute("pokemon_name") == "venusaur"  # Should still be Venusaur

def test_evolution_changes_base_stats_not_level():
    """Test that evolution changes base stats but keeps current level stats properly scaled"""
    squirtle = Pokemon("squirtle", 7, "water", "blue", "male", level=20)
    
    squirtle_stats = squirtle.get_stats()
    squirtle_level_20_hp = squirtle_stats.hp
    
    # Evolve to Wartortle
    assert squirtle.evolve() is True
    
    wartortle_stats = squirtle.get_stats()
    
    # Base stats should be Wartortle's
    assert wartortle_stats.base_hp == 59  # Wartortle base
    assert squirtle_stats.base_hp == 44  # Squirtle base
    
    # But level should still be 20
    assert squirtle.get_attribute("level") == 20
    
    # And current HP should reflect Wartortle's higher base at level 20
    assert wartortle_stats.hp > squirtle_level_20_hp 
    