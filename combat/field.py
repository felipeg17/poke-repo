### TODO: Implement the battle field logic
# Turns management
# Uses engine to compute damage and update stats
# Defines win/loss conditions

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports
from pokemon.pokemon import Pokemon, Move
from combat.engine import CombatEngine
import pandas as pd


class Trainer:
    """Represents a Pokémon trainer with a selectable team.

    Attributes
    ----------
    name : str
        Trainer's name.
    pokemon : list[Pokemon]
        List of the trainer's Pokémon objects.
    """

    def __init__(self, name: str):
        self.name = name
        self.pokemon = []

    def pokemon_available(self, pokemon_used=None):
        """Return a DataFrame of available Pokémon filtered by `pokemon_used`.

        Parameters
        ----------
        pokemon_used : list[str] | None
            Names of Pokémon already chosen (to exclude from the list).
        """
        df = pd.read_csv(Pokemon.csv_path)
        if pokemon_used:
            df = df[~df["pokemon_name"].isin(pokemon_used)]

        return df

    def choose_pokemon(self):
        """Interactively choose up to 3 Pokémon for this trainer.
        Prompts the user to enter a pokédex number and the Pokémon's type.
        Returns the list of chosen `Pokemon` objects.
        """
        while True:
            print(
                f"{self.name}, choose Pokémon #{len(self.pokemon) + 1} for the battle."
            )

            already_chosen = [p.get_attribute("pokemon_name") for p in self.pokemon]
            df = self.pokemon_available(already_chosen)

            while True:
                try:
                    chosen = int(input("Enter pokedex number: ").strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            row = df.loc[df["pokedex_number"] == chosen]
            if row.empty:
                print("Invalid number. Try again.")
                continue
            row = row.iloc[0]
            name = row["pokemon_name"]
            pokedex_number = int(row["pokedex_number"])

            poke_type = row["type1"]
            poke_type2 = row["type2"]
            while True:
                try:
                    level = int(input(f"Enter the level for {name} (1-100): "))
                    if level >= 1 and level <= 100:
                        break
                    else:
                        print("Level must be between 1 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            self.pokemon.append(
                Pokemon(
                    name, pokedex_number, poke_type, poke_type2, "gray", "male", level
                )
            )
            print(f"\n {self.name} chose {name} for the battle!")

            if len(self.pokemon) == 1:
                print("This is your full team for the battle.")
                for pkm in self.pokemon:
                    print(
                        f"{pkm.get_attribute('pokedex_num')} - {pkm.get_attribute('pokemon_name')} - level {pkm.get_attribute('level')}"
                    )
                while True:
                    print("Do you want to proceed with this team? (y/n)")
                    confirm = input().strip().lower()
                    if confirm == "y" or confirm == "n":
                        break
                    else:
                        print("Invalid input, try again.")
                        continue
                if confirm == "n":
                    self.pokemon = []
                    continue
                break
        return self.pokemon


class Field:
    """Manage a battle between two `Trainer` instances.

    Responsibilities:
    - Track each trainer's team and active Pokémon
    - Keep combat HP for each Pokémon
    - Handle turns, switches, attacks
    """

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.__team1 = trainer1.pokemon.copy()
        self.__team2 = trainer2.pokemon.copy()
        self.__active1 = self.__team1[0] if self.__team1 else None
        self.__active2 = self.__team2[0] if self.__team2 else None
        self.__combat_hp = {}
        self.__number_turn = 0
        self.active1_moves = []
        self.active2_moves = []

        for pokemon in self.__team1:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp

        for pokemon in self.__team2:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp

    def get_team1(self):
        return self.__team1

    def get_team2(self):
        return self.__team2

    def get_active1(self):
        return self.__active1

    def get_active2(self):
        return self.__active2

    def get_number_turn(self):
        return self.__number_turn

    def get_combat_hp(self, pokemon):
        return self.__combat_hp.get(pokemon, 0)

    def set_combat_hp(self, pokemon, value):
        self.__combat_hp[pokemon] = max(0, value)

    """Apply damage to pokemon, can't go below 0"""

    def reduce_hp(self, pokemon, damage):
        current = self.get_combat_hp(pokemon)
        self.set_combat_hp(pokemon, current - damage)

    def end_battle(self):
        """True if at least one team is completely defeated"""
        team1_alive = any(self.get_combat_hp(p) > 0 for p in self.__team1)
        team2_alive = any(self.get_combat_hp(p) > 0 for p in self.__team2)
        return not (team1_alive and team2_alive)

    def winner_game(self):
        """Returns winner or None if battle isn't over"""
        if not self.end_battle():
            return None
        team1_alive = any(self.get_combat_hp(p) > 0 for p in self.__team1)
        return self.trainer1 if team1_alive else self.trainer2

    def pokemon_available(self, trainer):
        """Get list of Pokémon that can still battle for a trainer"""
        if trainer == self.trainer1:
            team = self.__team1
            active = self.__active1
        else:
            team = self.__team2
            active = self.__active2

        available = []
        for pokemon in team:
            if self.get_combat_hp(pokemon) > 0 and pokemon != active:
                available.append(pokemon)

        return available

    def switch_defeat(self, trainer):
        """True if active pokemon fainted and trainer has replacements"""
        active = self.__active1 if trainer == self.trainer1 else self.__active2
        if active is None:
            return False
        return (
            self.get_combat_hp(active) <= 0 and len(self.pokemon_available(trainer)) > 0
        )

    def switch_pokemon(self, trainer, new_pokemon):
        """Switch active Pokémon for a trainer"""
        if new_pokemon not in trainer.pokemon:
            return False

        if self.get_combat_hp(new_pokemon) <= 0:
            return False

        if trainer == self.trainer1:
            if new_pokemon == self.__active1:
                return False
            self.__active1 = new_pokemon
        else:
            if new_pokemon == self.__active2:
                return False
            self.__active2 = new_pokemon

        return True

    def execute_attack(
        self,
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        attacker_moves: list,
        defender_moves: list,
    ):
        """Execute an attack from attacker to defender using the specified move."""
        engine = CombatEngine(
            attacker=attacker,
            defender=defender,
            move=move,
            attacker_moves=attacker_moves,
            defender_moves=defender_moves,
        )

        damage, was_critical = engine.calculate_damage()
        if damage == 0:
            return (0, False, "The attack missed!")

        self.reduce_hp(defender, damage)
        effectiveness = defender.receive_attack(move.type)

        message = f"It dealt {damage} damage!"
        if was_critical:
            message += " A critical hit!"
        message += f" {effectiveness}"

        return (damage, was_critical, message)

    def resolve_turn(self, action1, action2):
        """
        Execute a turn based on both players' actions.
        if action is "surrender", the battle ends.
        if action is "switch", the active Pokémon is switched.
        if action is "attack", the active Pokémon attacks the opponent's active Pokémon.

        """

        self.__number_turn += 1
        messages = []

        if action1["action"] == "surrender":
            messages.append(f"{self.trainer1.name} surrendered!")
            messages.append(f"{self.trainer2.name} won the battle!")
            return (False, messages)

        if action2["action"] == "surrender":
            messages.append(f"{self.trainer2.name} surrendered!")
            messages.append(f"{self.trainer1.name} won the battle!")
            return (False, messages)

        if action1["action"] == "switch" and action2["action"] == "switch":
            self.__active1 = action1["new_pokemon"]
            self.active1_moves = []
            messages.append(f"{self.trainer1.name} sent out {self.__active1._name}!")

            self.__active2 = action2["new_pokemon"]
            self.active2_moves = []
            messages.append(f"{self.trainer2.name} sent out {self.__active2._name}!")
            return (True, messages)

        elif action1["action"] == "switch":
            self.__active1 = action1["new_pokemon"]
            self.active1_moves = []
            messages.append(f"{self.trainer1.name} sent out {self.__active1._name}!")

            if action2["action"] == "attack":
                messages.append(self.__active2.attack())
                messages.append(f"{self.__active2._name} used {action2['move'].name}!")
                self.active2_moves.append(action2["move"])
                damage, crit, msg = self.execute_attack(
                    self.__active2,
                    self.__active1,
                    action2["move"],
                    self.active2_moves,
                    self.active1_moves,
                )
                messages.append(msg)
            return (True, messages)

        elif action2["action"] == "switch":
            self.__active2 = action2["new_pokemon"]
            self.active2_moves = []
            messages.append(f"{self.trainer2.name} sent out {self.__active2._name}!")

            if action1["action"] == "attack":
                messages.append(self.__active1.attack())
                messages.append(f"{self.__active1._name} used {action1['move'].name}!")
                self.active1_moves.append(action1["move"])
                damage, crit, msg = self.execute_attack(
                    self.__active1,
                    self.__active2,
                    action1["move"],
                    self.active1_moves,
                    self.active2_moves,
                )
                messages.append(msg)
            return (True, messages)

        if action1["action"] == "attack" and action2["action"] == "attack":
            if self.__active1.get_stats().speed >= self.__active2.get_stats().speed:
                messages.append(f"{self.__active1._name} is faster!")
                print(self.__active1.attack())
                messages.append(f"{self.__active1._name} used {action1['move'].name}!")
                self.active1_moves.append(action1["move"])
                damage, crit, msg = self.execute_attack(
                    self.__active1,
                    self.__active2,
                    action1["move"],
                    self.active1_moves,
                    self.active2_moves,
                )
                messages.append(msg)

                if self.get_combat_hp(self.__active2) > 0:
                    print(self.__active2.attack())
                    messages.append(
                        f"{self.__active2._name} used {action2['move'].name}!"
                    )
                    self.active2_moves.append(action2["move"])
                    damage, crit, msg = self.execute_attack(
                        self.__active2,
                        self.__active1,
                        action2["move"],
                        self.active2_moves,
                        self.active1_moves,
                    )
                    messages.append(msg)
            else:
                messages.append(f"{self.__active2._name} is faster!")
                messages.append(self.__active2.attack())
                messages.append(f"{self.__active2._name} used {action2['move'].name}!")
                self.active2_moves.append(action2["move"])
                damage, crit, msg = self.execute_attack(
                    self.__active2,
                    self.__active1,
                    action2["move"],
                    self.active2_moves,
                    self.active1_moves,
                )
                messages.append(msg)

                if self.get_combat_hp(self.__active1) > 0:
                    messages.append(self.__active1.attack())
                    messages.append(
                        f"{self.__active1._name} used {action1['move'].name}!"
                    )
                    self.active1_moves.append(action1["move"])
                    damage, crit, msg = self.execute_attack(
                        self.__active1,
                        self.__active2,
                        action1["move"],
                        self.active1_moves,
                        self.active2_moves,
                    )
                    messages.append(msg)

            return (True, messages)

        return (True, messages)

    def remove_defeated_pokemon(self):
        """
        Check for defeated Pokémon and remove them from teams.
        """
        messages = []
        needs_switch1 = False
        needs_switch2 = False

        if self.__active1 and self.get_combat_hp(self.__active1) <= 0:
            messages.append(f"{self.__active1._name} defeated!")
            self.__team1.remove(self.__active1)

            if len(self.__team1) > 0:
                needs_switch1 = True
            else:
                messages.append(f"{self.trainer2.name} wins the battle!")
                messages.append(f"{self.trainer1.name} has no Pokémon left!")

        if self.__active2 and self.get_combat_hp(self.__active2) <= 0:
            messages.append(f"{self.__active2._name} defeated!")
            self.__team2.remove(self.__active2)

            if len(self.__team2) > 0:
                needs_switch2 = True
            else:
                messages.append(f"{self.trainer1.name} wins the battle!")
                messages.append(f"{self.trainer2.name} has no Pokémon left!")

        return (needs_switch1, needs_switch2, messages)

    def health_bar(self, current_hp, max_hp, bar_length=20):
        """
        Return a simple text health bar representation.
        """
        if max_hp <= 0:
            bar = "░" * bar_length
            return f"[{bar}] 0/0 HP"
        filled = int((current_hp / max_hp) * bar_length)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty

        return f"[{bar}] {current_hp}/{max_hp} HP"


class Battle:
    """All interactions for battles

    Responsibilities:
    - Display battle and turn headers
    - Show battle status
    - Prompt trainers for actions
    - Display messages
    - Manage the battle loop
    """

    def __init__(self, field: Field):
        self.field = field

    def display_battle_header(self):
        """Display the battle header"""
        print(60 * "=")
        print(f"{self.field.trainer1.name} VS {self.field.trainer2.name}")
        print(60 * "=")

    def display_turn_header(self):
        """Display the turn header"""
        print("\n" + 60 * "=")
        print(f"TURN #{self.field.get_number_turn() + 1}")
        print(60 * "=")

    def display_battle_status(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ):
        """Display the current battle status"""
        active_hp = self.field.get_combat_hp(active_pokemon)
        enemy_hp = self.field.get_combat_hp(enemy_pokemon)

        print(f"""
        {50 * "="}
        Turn: {trainer.name}
        {active_pokemon._name:<20} VS {enemy_pokemon._name:>20}
        {self.field.health_bar(active_hp, active_pokemon._stats.hp)}  {self.field.health_bar(enemy_hp, enemy_pokemon._stats.hp)}
        {50 * "="}
        """)

    def action_py(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ):
        """Prompt the trainer for an action during their turn"""
        self.display_battle_status(trainer, active_pokemon, enemy_pokemon)

        choice = int(
            input("""
              (1) Attack
              (2) Switch Pokémon
              (0) Surrender
              """)
        )

        if choice == 1:
            return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
        elif choice == 2:
            return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
        elif choice == 0:
            return self.choice_surrender(trainer)
        else:
            print("Invalid choice. Try again.")
            return self.action_py(trainer, active_pokemon, enemy_pokemon)

    def choice_attack(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ):
        """Prompt the trainer to choose an attack move"""
        moves = active_pokemon.get_moveset().current_moves

        print(f"\n{30 * '='}")
        print(" Attacks:")
        for i, move in enumerate(moves, 1):
            print(f"({i}) {move}")
        print(f"{30 * '='}")

        try:
            choice_move = int(input("Choose (0 to go back): "))
            if choice_move == 0:
                return self.action_py(trainer, active_pokemon, enemy_pokemon)
            elif 1 <= choice_move <= len(moves):
                chosen_move = moves[choice_move - 1]
                if chosen_move.pp == 0:
                    print("No PP left for this move. Choose another one.")
                    return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
                print(f"{active_pokemon._name} will use {chosen_move.name}!")
                chosen_move.pp -= 1
                return {"action": "attack", "move": chosen_move}
            else:
                print("Invalid choice.")
                return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
        except ValueError:
            print("Enter a valid number.")
            return self.choice_attack(trainer, active_pokemon, enemy_pokemon)

    def choice_switch(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ):
        """Prompt the trainer to choose a Pokémon to switch to"""
        team = trainer.pokemon
        print(f"{30 * '='}")
        print("Your team:")

        for i, pokemon in enumerate(team, 1):
            current_hp = self.field.get_combat_hp(pokemon)
            max_hp = pokemon._stats.hp
            hp_bar = self.field.health_bar(current_hp, max_hp, bar_length=15)

            if pokemon == active_pokemon:
                status = " - (Active)"
            elif current_hp <= 0:
                status = " (defeated)"
            else:
                status = ""

            print(f"({i}) {pokemon._name} {hp_bar}{status}")
        print(f"{30 * '='}")

        try:
            choice_pkm = int(input("\nChoose a Pokémon (0 to go back): "))

            if choice_pkm == 0:
                return self.action_py(trainer, active_pokemon, enemy_pokemon)
            elif 1 <= choice_pkm <= len(team):
                new_pokemon = team[choice_pkm - 1]

                if new_pokemon == active_pokemon:
                    print("That Pokémon is already in battle!")
                    return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
                elif self.field.get_combat_hp(new_pokemon) <= 0:
                    print("That Pokémon has been defeated!")
                    return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
                else:
                    print(f"Go, {new_pokemon._name}!")
                    return {"action": "switch", "new_pokemon": new_pokemon}
            else:
                print("Invalid option.")
                return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
        except ValueError:
            print("Enter a valid number.")
            return self.choice_switch(trainer, active_pokemon, enemy_pokemon)

    def choice_surrender(self, trainer: Trainer):
        """Prompt the trainer to confirm surrendering"""
        confirm = input(f"Are you sure you want to surrender, {trainer.name}? (y/n) ")
        if confirm.lower() == "y":
            return {"action": "surrender"}
        else:
            print("Surrender cancelled.")
            return self.action_py(
                trainer,
                self.field.get_active1()
                if trainer == self.field.trainer1
                else self.field.get_active2(),
                self.field.get_active2()
                if trainer == self.field.trainer1
                else self.field.get_active1(),
            )

    def switch_after_defeat(self, trainer: Trainer):
        """Prompt the trainer to choose their next Pokémon after one is defeated"""
        print(f"\n{trainer.name}, choose your next Pokémon:")
        available = self.field.pokemon_available(trainer)

        for i, pokemon in enumerate(available, 1):
            current_hp = self.field.get_combat_hp(pokemon)
            max_hp = pokemon._stats.hp
            hp_bar = self.field.health_bar(current_hp, max_hp, bar_length=15)
            print(f"({i}) {pokemon._name} {hp_bar}")

        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(available):
                    new_pokemon = available[choice]
                    print(f"Go, {new_pokemon._name}!")
                    self.field.switch_pokemon(trainer, new_pokemon)
                    return new_pokemon
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Enter a valid number.")

    def display_messages(self, messages):
        for msg in messages:
            print(msg)

    def battle(self):
        """Main battle loop"""
        self.display_battle_header()
        while not self.field.end_battle():
            self.display_turn_header()

            action1 = self.action_py(
                self.field.trainer1, self.field.get_active1(), self.field.get_active2()
            )

            action2 = self.action_py(
                self.field.trainer2, self.field.get_active2(), self.field.get_active1()
            )

            continue_battle, messages = self.field.resolve_turn(action1, action2)
            self.display_messages(messages)

            if not continue_battle:
                break

            needs_switch1, needs_switch2, defeated_messages = (
                self.field.remove_defeated_pokemon()
            )
            self.display_messages(defeated_messages)

            if self.field.end_battle():
                break

            if needs_switch1:
                self.switch_after_defeat(self.field.trainer1)

            if needs_switch2:
                self.switch_after_defeat(self.field.trainer2)

        winner = self.field.winner_game()
        if winner:
            print(f"\n🎉 {winner.name} is the winner!")

    def main_menu():
        """Main game loop with restart menu"""
        print("=" * 60)
        print("POKÉMON BATTLE SIMULATOR")
        print("=" * 60)

        while True:
            print("\n" + "=" * 60)

            trainer1_name = input("Trainer 1 name: ")
            trainer2_name = input("Trainer 2 name: ")

            trainer1 = Trainer(trainer1_name)
            trainer2 = Trainer(trainer2_name)

            print("\n" + "=" * 60)
            trainer1.choose_pokemon()

            print("\n" + "=" * 60)
            trainer2.choose_pokemon()

            print("\n" + "=" * 60)
            print("BATTLE START!")
            print("=" * 60)

            field = Field(trainer1, trainer2)
            battle = Battle(field)
            battle.battle()

            print("\n" + "=" * 60)
            print("BATTLE END")
            print("=" * 60)

            while True:
                option = input(
                    "\nWhat do you want to do?\n(1) Play again\n(2) Exit\n> "
                ).strip()

                if option == "1":
                    print("\n" + "=" * 60)
                    print("NEW BATTLE")
                    print("=" * 60)
                    break
                elif option == "2":
                    print("\nThanks for playing! See you later!")
                    return
                else:
                    print("Invalid option. Choose 1 or 2.")
