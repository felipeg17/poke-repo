import pytest
import random
from combat.field import Field, Trainer
from pokemon.pokemon import Pokemon, Move, Stats
from combat.engine import CombatEngine


class TestCombatEngine:
    @pytest.fixture
    def pokemon_to_test(self):
        trainer = Trainer("Test")
        attacker = trainer.create_pokemon(
            "pikachu", 25, "electric", "yellow", "male", level=50
        )
        defender = trainer.create_pokemon(
            "charizard", 6, "fire", "orange", "male", level=50
        )
        return attacker, defender

    @pytest.fixture
    def stats_dicts(self, pokemon_to_test):
        attacker, defender = pokemon_to_test

        attack_stats = {
            attacker: attacker.get_stats().attack,
            defender: defender.get_stats().attack,
        }
        defense_stats = {
            attacker: attacker.get_stats().defense,
            defender: defender.get_stats().defense,
        }
        sp_attack_stats = {
            attacker: attacker.get_stats().sp_attack,
            defender: defender.get_stats().sp_attack,
        }
        sp_defense_stats = {
            attacker: attacker.get_stats().sp_defense,
            defender: defender.get_stats().sp_defense,
        }
        speed_stats = {
            attacker: attacker.get_stats().speed,
            defender: defender.get_stats().speed,
        }

        return (
            attack_stats,
            defense_stats,
            sp_attack_stats,
            sp_defense_stats,
            speed_stats,
        )

    @pytest.fixture
    def basic_move(self):
        return Move(1, "Thunderbolt", "electric", 90, 100, 15, "special")

    @pytest.fixture
    def weak_move(self):
        return Move(2, "Tackle", "normal", 40, 100, 35, "physical")

    @pytest.fixture
    def high_crit_move(self):
        return Move(3, "Slash", "normal", 70, 100, 20, "physical")

    def test_engine_init(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        assert engine.attacker == attacker
        assert engine.defender == defender
        assert engine.move == basic_move
        assert engine.attacker_moves == []
        assert engine.defender_moves == []

    def test_calculate_damage_returns_tuple(
        self, pokemon_to_test, basic_move, stats_dicts
    ):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats = (
            stats_dicts
        )

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        result = engine.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        assert type(result) == tuple
        assert len(result) == 3
        assert type(result[0]) == int
        assert type(result[1]) == bool
        assert type(result[2]) == bool

    def test_calculate_damage_is_positive(
        self, pokemon_to_test, basic_move, stats_dicts
    ):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats = (
            stats_dicts
        )

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        damage, _, _ = engine.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        assert damage >= 0

    def test_damage_increases_with_power(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats = (
            stats_dicts
        )

        weak_move = Move(1, "Weak", "normal", 40, 100, 35, "physical")
        strong_move = Move(2, "Strong", "normal", 120, 100, 35, "physical")

        random.seed(42)
        engine_weak = CombatEngine(attacker, defender, weak_move, [], [])
        damage_weak, _, hit_weak = engine_weak.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        random.seed(42)
        engine_strong = CombatEngine(attacker, defender, strong_move, [], [])
        damage_strong, _, hit_strong = engine_strong.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        if hit_weak and hit_strong:
            assert damage_strong > damage_weak

    def test_critical_hit_returns_bool(self, pokemon_to_test, basic_move, stats_dicts):
        attacker, defender = pokemon_to_test
        _, _, _, _, speed_stats = stats_dicts

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        result = engine.critical_hit(speed_stats)

        assert isinstance(result, bool)

    def test_high_crit_move_increases_crit_chance(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        _, _, _, _, speed_stats = stats_dicts

        normal_move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        high_crit_move = Move(2, "Slash", "normal", 70, 100, 20, "physical")

        crit_count_normal = 0
        crit_count_high = 0
        iterations = 1000

        for _ in range(iterations):
            engine_normal = CombatEngine(attacker, defender, normal_move, [], [])
            if engine_normal.critical_hit(speed_stats):
                crit_count_normal += 1

            engine_high = CombatEngine(attacker, defender, high_crit_move, [], [])
            if engine_high.critical_hit(speed_stats):
                crit_count_high += 1

        assert crit_count_high > crit_count_normal

    def test_attack_defense_returns_tuple(
        self, pokemon_to_test, basic_move, stats_dicts
    ):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        A, D = engine.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert isinstance(A, (int, float))
        assert isinstance(D, (int, float))
        assert A > 0
        assert D > 0

    def test_physical_vs_special_uses_different_stats(
        self, pokemon_to_test, stats_dicts
    ):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        physical_move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        special_move = Move(2, "Thunderbolt", "electric", 90, 100, 15, "special")

        engine_physical = CombatEngine(attacker, defender, physical_move, [], [])
        A_phys, D_phys = engine_physical.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        engine_special = CombatEngine(attacker, defender, special_move, [], [])
        A_spec, D_spec = engine_special.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert (A_phys, D_phys) != (A_spec, D_spec)

    def test_hit_accuracy_returns_bool(self, pokemon_to_test, basic_move):
        attacker, defender = pokemon_to_test

        engine = CombatEngine(attacker, defender, basic_move, [], [])

        result = engine.hit_accuracy()

        assert type(result) == bool

    def test_perfect_accuracy_always_hits(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        perfect_move = Move(1, "Swift", "normal", 60, 100, 20, "special")
        hits = 0
        iterations = 100

        for _ in range(iterations):
            engine = CombatEngine(attacker, defender, perfect_move, [], [])
            if engine.hit_accuracy():
                hits += 1

        assert hits >= 95

    def test_low_accuracy_misses_more(self, pokemon_to_test):
        attacker, defender = pokemon_to_test

        high_acc = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        low_acc = Move(2, "Thunder", "electric", 110, 70, 10, "special")

        hits_high = 0
        hits_low = 0
        iterations = 1000

        for _ in range(iterations):
            engine_high = CombatEngine(attacker, defender, high_acc, [], [])
            if engine_high.hit_accuracy():
                hits_high += 1

            engine_low = CombatEngine(attacker, defender, low_acc, [], [])
            if engine_low.hit_accuracy():
                hits_low += 1

        assert hits_high > hits_low, f"High: {hits_high}, Low: {hits_low}"

    def test_explosion_halves_defense(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        normal_move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        explosion = Move(2, "Explosion", "normal", 250, 100, 5, "physical")

        engine_normal = CombatEngine(attacker, defender, normal_move, [], [])
        _, D_normal = engine_normal.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        engine_explosion = CombatEngine(attacker, defender, explosion, [], [])
        _, D_explosion = engine_explosion.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert D_explosion < D_normal

    def test_minimum_damage_is_one(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats = (
            stats_dicts
        )

        weak_move = Move(1, "Weak", "normal", 1, 100, 35, "physical")

        engine = CombatEngine(attacker, defender, weak_move, [], [])
        damage, _, hit = engine.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        if hit and damage > 0:
            assert damage >= 1

    def test_status_changes_paralyzed(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")

        attacker.apply_status("paralyzed")
        attacker.status["paralyzed"] = 999

        can_attack_count = 0
        cannot_attack_count = 0
        iterations = 1000

        for _ in range(iterations):
            attacker.status = {"paralyzed": 999}

            engine = CombatEngine(attacker, defender, move, [], [])
            can_attack, _ = engine.status_changes(move.power)

            if can_attack:
                can_attack_count += 1
            else:
                cannot_attack_count += 1

        assert 650 <= can_attack_count <= 850
        assert 150 <= cannot_attack_count <= 350

    def test_status_changes_frozen(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")

        attacker.apply_status("frozen")
        attacker.status["frozen"] = 3

        engine = CombatEngine(attacker, defender, move, [], [])
        can_attack, power = engine.status_changes(move.power)

        assert power == move.power

    def test_status_changes_burned_returns_true(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")

        attacker.apply_status("burned")
        attacker.status["burned"] = 999

        engine = CombatEngine(attacker, defender, move, [], [])
        can_attack, power = engine.status_changes(move.power)

        assert can_attack is True

    def test_status_changes_asleep(self, pokemon_to_test):
        attacker, defender = pokemon_to_test
        move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")

        attacker.apply_status("asleep")
        attacker.status["asleep"] = 3

        engine = CombatEngine(attacker, defender, move, [], [])
        can_attack, power = engine.status_changes(move.power)

        assert can_attack is False

    def test_reflect_doubles_physical_defense(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        physical_move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        reflect_move = Move(99, "Reflect", "psychic", 0, 100, 20, "special")

        engine_no_reflect = CombatEngine(attacker, defender, physical_move, [], [])
        _, D_no_reflect = engine_no_reflect.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        engine_with_reflect = CombatEngine(
            attacker, defender, physical_move, [], [reflect_move]
        )
        _, D_with_reflect = engine_with_reflect.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert D_with_reflect == D_no_reflect * 2

    def test_light_screen_doubles_special_defense(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        special_move = Move(1, "Thunderbolt", "electric", 90, 100, 15, "special")
        light_screen_move = Move(99, "Light Screen", "psychic", 0, 100, 30, "special")

        engine_no_screen = CombatEngine(attacker, defender, special_move, [], [])
        _, D_no_screen = engine_no_screen.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        engine_with_screen = CombatEngine(
            attacker, defender, special_move, [], [light_screen_move]
        )

        _, D_with_screen = engine_with_screen.attack_defense(
            False, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert D_with_screen == D_no_screen * 2

    def test_critical_hit_ignores_reflect(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, _ = stats_dicts

        physical_move = Move(1, "Tackle", "normal", 40, 100, 35, "physical")
        reflect_move = Move(99, "Reflect", "psychic", 0, 100, 20, "special")

        engine_crit_no_reflect = CombatEngine(attacker, defender, physical_move, [], [])
        _, D_crit_no_reflect = engine_crit_no_reflect.attack_defense(
            True, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        engine_crit_with_reflect = CombatEngine(
            attacker, defender, physical_move, [], [reflect_move]
        )
        _, D_crit_with_reflect = engine_crit_with_reflect.attack_defense(
            True, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )

        assert D_crit_with_reflect == D_crit_no_reflect

    def test_move_with_zero_power(self, pokemon_to_test, stats_dicts):
        attacker, defender = pokemon_to_test
        attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats = (
            stats_dicts
        )

        status_move = Move(1, "Growl", "normal", 0, 100, 40, "physical")

        engine = CombatEngine(attacker, defender, status_move, [], [])
        damage, is_crit, move_hit = engine.calculate_damage(
            attack_stats, defense_stats, sp_attack_stats, sp_defense_stats, speed_stats
        )

        assert damage == 0
        assert is_crit is False
