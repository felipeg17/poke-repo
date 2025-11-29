import pytest
from combat.field import Field, Trainer
from pokemon.pokemon import Pokemon, Move, Stats
from combat.engine import CombatEngine


class TestField:
    @pytest.fixture
    def trainers(self):
        trainer1 = Trainer("Ash")
        trainer2 = Trainer("Gary")

        trainer1.pokemon = [
            trainer1.create_pokemon(
                "pikachu", 25, "Electric", "yellow", "male", level=10
            ),
            trainer1.create_pokemon(
                "charmander", 4, "Fire", "orange", "male", level=10
            ),
        ]
        trainer2.pokemon = [
            trainer2.create_pokemon("squirtle", 7, "Water", "blue", "male", level=10),
            trainer2.create_pokemon("bulbasaur", 1, "Grass", "green", "male", level=10),
        ]

        return trainer1, trainer2

    def test_field_init(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        assert field.trainer1 == trainer1
        assert field.trainer2 == trainer2
        assert len(field.get_team1()) == 2
        assert len(field.get_team2()) == 2
        assert field.get_active1() is not None
        assert field.get_active2() is not None

    def test_combat_hp_init(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]
        squirtle = trainer2.pokemon[0]

        assert field.get_combat_hp(pikachu) == pikachu.get_stats().hp
        assert field.get_combat_hp(squirtle) == squirtle.get_stats().hp

    def test_reduce_hp(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]
        initial_hp = field.get_combat_hp(pikachu)

        field.reduce_hp(pikachu, 20)

        assert field.get_combat_hp(pikachu) == initial_hp - 20

    def test_reduce_hp_cannot_go_negative(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]
        field.reduce_hp(pikachu, 9999)

        assert field.get_combat_hp(pikachu) == 0

    def test_health_bar(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        bar = field.health_bar(100, 100, bar_length=10)
        assert "█" in bar
        assert "100/100" in bar

        bar = field.health_bar(50, 100, bar_length=10)
        assert "50/100" in bar

    def test_set_combat_hp(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]

        field.set_combat_hp(pikachu, 50)
        assert field.get_combat_hp(pikachu) == 50

    def test_surrender_ends_battle(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")

        continue_battle, messages = field.resolve_turn(
            {"action": "surrender"}, {"action": "attack", "move": move}
        )

        assert continue_battle is False
        assert any("surrendered" in msg for msg in messages)

    def test_both_surrender_ends_battle(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        continue_battle, messages = field.resolve_turn(
            {"action": "surrender"}, {"action": "surrender"}
        )

        assert continue_battle is False

    def test_switch_pokemon(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        initial_active1 = field.get_active1()
        initial_active2 = field.get_active2()

        continue_battle, messages = field.resolve_turn(
            {"action": "switch", "new_pokemon": trainer1.pokemon[1]},
            {"action": "switch", "new_pokemon": trainer2.pokemon[1]},
        )

        assert continue_battle is True
        assert field.get_active1() == trainer1.pokemon[1]
        assert field.get_active2() == trainer2.pokemon[1]
        assert field.get_active1() != initial_active1
        assert field.get_active2() != initial_active2

    def test_attack_reduces_hp(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")

        current_active1 = field.get_active1()
        current_active2 = field.get_active2()

        hp_before1 = field.get_combat_hp(current_active1)
        hp_before2 = field.get_combat_hp(current_active2)

        continue_battle, messages = field.resolve_turn(
            {"action": "attack", "move": move}, {"action": "attack", "move": move}
        )

        assert continue_battle is True

        assert (
            field.get_combat_hp(current_active1) < hp_before1
            or field.get_combat_hp(current_active2) < hp_before2
        )

    def test_faster_pokemon_attacks_first(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")

        speed1 = field.get_combat_speed(field.get_active1())
        speed2 = field.get_combat_speed(field.get_active2())

        continue_battle, messages = field.resolve_turn(
            {"action": "attack", "move": move}, {"action": "attack", "move": move}
        )

        if speed1 >= speed2:
            assert any(
                "is faster" in msg and field.get_active1()._name in msg
                for msg in messages
            )
        else:
            assert any(
                "is faster" in msg and field.get_active2()._name in msg
                for msg in messages
            )

    def test_end_battle(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        assert field.end_battle() is False

        for pokemon in field.get_team2():
            field.set_combat_hp(pokemon, 0)

        assert field.end_battle() is True

    def test_winner_game(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        assert field.winner_game() is None

        for pokemon in field.get_team2():
            field.set_combat_hp(pokemon, 0)

        assert field.winner_game() == trainer1

    def test_pokemon_knockout_removes_from_team(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        field.set_combat_hp(field.get_active2(), 0)

        initial_team_size = len(field.get_team2())

        needs_switch1, needs_switch2, messages = field.remove_defeated_pokemon()

        assert len(field.get_team2()) == initial_team_size - 1
        assert needs_switch2 is True
        assert any("defeated" in msg for msg in messages)

    def test_pokemon_available(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        available = field.pokemon_available(trainer1)
        assert len(available) == 1
        assert field.get_active1() not in available

        for pokemon in field.get_team1():
            if pokemon != field.get_active1():
                field.set_combat_hp(pokemon, 0)

        available = field.pokemon_available(trainer1)
        assert len(available) == 0

    def test_switch_pokemon_method(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        new_pokemon = trainer1.pokemon[1]

        success = field.switch_pokemon(trainer1, new_pokemon)

        assert success is True
        assert field.get_active1() == new_pokemon

        success = field.switch_pokemon(trainer1, new_pokemon)
        assert success is False

    def test_execute_attack_returns_damage_info(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")

        attacker = field.get_active1()
        defender = field.get_active2()

        damage, was_critical, message = field.execute_attack(
            attacker, defender, move, [], []
        )

        assert isinstance(damage, int)
        assert isinstance(was_critical, bool)
        assert isinstance(message, str)
        assert damage >= 0

    def test_switch_defeat(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        assert field.switch_defeat(trainer1) is False

        field.set_combat_hp(field.get_active1(), 0)

        assert field.switch_defeat(trainer1) is True

    def test_turn_counter(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        assert field.get_number_turn() == 0

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")
        field.resolve_turn(
            {"action": "attack", "move": move}, {"action": "attack", "move": move}
        )

        assert field.get_number_turn() == 1

    def test_switch_then_attack(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        move = Move(150, "TestMove", "Normal", 40, 255, 10, "Physical")

        initial_active2 = field.get_active2()
        new_pokemon = trainer2.pokemon[1]

        continue_battle, messages = field.resolve_turn(
            {"action": "attack", "move": move},
            {"action": "switch", "new_pokemon": new_pokemon},
        )

        assert field.get_active2() == new_pokemon
        assert field.get_active2() != initial_active2

        assert field.get_combat_hp(new_pokemon) < new_pokemon.get_stats().hp

        assert any("sent out" in msg for msg in messages)
        assert any("used TestMove" in msg for msg in messages)

    def test_combat_stats_modifiers(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]
        initial_attack = field.get_combat_attack(pikachu)

        field.mod_combat_attack(pikachu, 10)
        assert field.get_combat_attack(pikachu) == initial_attack + 10

        field.mod_combat_attack(pikachu, -5)
        assert field.get_combat_attack(pikachu) == initial_attack + 5

    def test_status_damage(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        pikachu = trainer1.pokemon[0]

        pikachu.apply_status("Burned")

        initial_hp = field.get_combat_hp(pikachu)

        message = field.status_damage(pikachu)

        assert field.get_combat_hp(pikachu) < initial_hp
        assert "Burned" in message

    def test_move_effect_basic(self, trainers):
        trainer1, trainer2 = trainers
        field = Field(trainer1, trainer2)

        attacker = trainer1.pokemon[0]
        defender = trainer2.pokemon[0]

        move = Move(150, "Growl", "Normal", 0, 100, 40, "Status")

        initial_attack = field.get_combat_attack(defender)

        damage, message = field.move_effect(move, attacker, defender, 0)

        assert field.get_combat_attack(defender) < initial_attack
        assert "fell" in message.lower()
