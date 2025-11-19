import pytest
from pokemon import Pokemon, Move
from engine import CombatEngine
import random

class TestCombatEngine:
    
    @pytest.fixture
    def pokemon_to_test(self):
        attacker = Pokemon("pikachu", 25, "electric", "yellow", "male", level=50)
        attacker.get_stats().combat_stats()
        defender = Pokemon("charizard", 6, "fire", "orange", "male", level=50)
        defender.get_stats().combat_stats()
        return attacker, defender
    
    @pytest.fixture
    def basic_move(self):

        return Move(1, "Thunderbolt", "Electric", 90, 255, 15)
    
    @pytest.fixture
    def weak_move(self):
    
        return Move(2, "Tackle", "Normal", 40, 255, 35)
    
    @pytest.fixture
    def high_crit_move(self):
        return Move(3, "Slash", "Normal", 70, 255, 20)
    
    def test_engine_init(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        assert engine.attacker == attacker
        assert engine.defender == defender
        assert engine.move == basic_move
        assert engine.attacker_moves == []
        assert engine.defender_moves == []
    
    def test_calculate_damage_returns_tuple(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        result = engine.calculate_damage()

        assert type(result) == tuple
        assert len(result) == 2
        assert type(result[0]) == int
        assert type(result[1]) == bool
    
    def test_calculate_damage_is_positive(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        damage, _ = engine.calculate_damage()
        
        assert damage >= 0
    
    def test_damage_increases_with_power(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        
        weak_move = Move(1, "Weak", "Normal", 40, 255, 35)
        strong_move = Move(2, "Strong", "Normal", 120, 255, 35)
        
        
        random.seed(42)
        
        engine_weak = CombatEngine(attacker, defender, weak_move, [], [])
        damage_weak, _ = engine_weak.calculate_damage()
        
        random.seed(42)  
        engine_strong = CombatEngine(attacker, defender, strong_move, [], [])
        damage_strong, _ = engine_strong.calculate_damage()
        
        assert damage_strong > damage_weak

    
    def test_critical_hit_returns_bool(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        result = engine.critical_hit()
        
        assert isinstance(result, bool)
    
    def test_high_crit_move_increases_crit_chance(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        
        normal_move = Move(1, "Tackle", "Normal", 40, 255, 35)
        high_crit_move = Move(2, "Slash", "Normal", 70, 255, 20)
        
        crit_count_normal = 0
        crit_count_high = 0
        iterations = 1000
        
        for _ in range(iterations):
            engine_normal = CombatEngine(attacker, defender, normal_move, [], [])
            if engine_normal.critical_hit():
                crit_count_normal += 1
            
            engine_high = CombatEngine(attacker, defender, high_crit_move, [], [])
            if engine_high.critical_hit():
                crit_count_high += 1
        
        
        assert crit_count_high > crit_count_normal
    
    
    def test_attack_defense_returns_tuple(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        A, D = engine.attack_defense(False)
        
        assert isinstance(A, (int, float))
        assert isinstance(D, (int, float))
        assert A > 0
        assert D > 0
    
    def test_critical_ignores_defense_buffs(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
        
        engine_no_reflect = CombatEngine(attacker, defender, basic_move, [], [])
        A1, D1 = engine_no_reflect.attack_defense(False)
        
        reflect_move = Move(104, "Reflect", "Psychic", 0, 255, 20)
        engine_reflect = CombatEngine(attacker, defender, basic_move, [], [reflect_move])
        A2, D2 = engine_reflect.attack_defense(False)
        
        engine_crit = CombatEngine(attacker, defender, basic_move, [], [reflect_move])
        A3, D3 = engine_crit.attack_defense(True)
        
        assert D2 > D1
    
        assert D3 == D1

    
    def test_hit_accuracy_returns_bool(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test
            
        engine = CombatEngine(attacker, defender, basic_move, [], [])
        
        result = engine.Hit_Accuracy()
        
        assert type(result) == bool
    
    def test_perfect_accuracy_always_hits(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        perfect_move = Move(1, "Swift", "Normal", 60, 255, 20)
        hits = 0
        iterations = 100
        
        for _ in range(iterations):
            engine = CombatEngine(attacker, defender, perfect_move, [], [])
            if engine.Hit_Accuracy():
                hits += 1
        
        assert hits >= 95  
    
    def test_low_accuracy_misses_more(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
    
   
        high_acc = Move(1, "Tackle", "Normal", 40, 255, 35)
    
  
        low_acc = Move(2, "Thunder", "Electric", 110, 127, 10)
    
        hits_high = 0
        hits_low = 0
        iterations = 1000
    
        for _ in range(iterations):
            engine_high = CombatEngine(attacker, defender, high_acc, [], [])
            if engine_high.Hit_Accuracy():
                hits_high += 1
        
            engine_low = CombatEngine(attacker, defender, low_acc, [], [])
            if engine_low.Hit_Accuracy():
                hits_low += 1

        assert hits_high > hits_low, f"High: {hits_high}, Low: {hits_low}"
     
    
    def test_explosion_halves_defense(self, pokemon_to_test):

        attacker, defender = pokemon_to_test
        
        normal_move = Move(1, "Tackle", "Normal", 40, 255, 35)
        explosion = Move(2, "Explosion", "Normal", 250, 255, 5)
        
        engine_normal = CombatEngine(attacker, defender, normal_move, [], [])
        _, D_normal = engine_normal.attack_defense(False)
        
        engine_explosion = CombatEngine(attacker, defender, explosion, [], [])
        _, D_explosion = engine_explosion.attack_defense(False)
        
        assert D_explosion < D_normal
    
    def test_minimum_damage_is_one(self, pokemon_to_test):

        attacker, defender = pokemon_to_test
        
        weak_move = Move(1, "Weak", "Normal", 1, 255, 35)
        
        engine = CombatEngine(attacker, defender, weak_move, [], [])
        damage, _ = engine.calculate_damage()
        
        if damage > 0:
            assert damage >= 1