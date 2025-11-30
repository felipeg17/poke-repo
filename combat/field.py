### TODO: Implement the battle field logic
# Turns management
# Uses engine to compute damage and update stats
# Defines win/loss conditions

from pokemon.pokemon import (
    Pokemon,
    Move,
    Normal,
    Fire,
    Water,
    Grass,
    Electric,
    Ice,
    Fighting,
    Poison,
    Ground,
    Flying,
    Psychic,
    Bug,
    Rock,
    Ghost,
    Dragon,
    Dark,
    Steel,
    Fairy,
)
from combat.engine import CombatEngine, math, random
import pandas as pd
from pandas import Series


class Trainer:
    """Represents a Pokémon trainer with a selectable team.

    Attributes:
        name (str): Trainer's name.
        pokemon (list[Pokemon]): List of the trainer's Pokémon objects.
    """

    def __init__(self, name: str):
        """Initializes a Trainer.

        Args:
            name (str): The trainer's name.
        """
        self.name = name
        self.pokemon: list[Pokemon] = []

    def pokemon_available(self, pokemon_used: list[str] | None = None) -> pd.DataFrame:
        """Returns a DataFrame of available Pokémon filtered by pokemon_used.

        Args:
            pokemon_used (list[str] | None, optional): Names of Pokémon already chosen
                to exclude from the list. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame with available Pokémon.
        """
        df = pd.read_csv(Pokemon.csv_path)
        if pokemon_used:
            df = df[~df["pokemon_name"].isin(pokemon_used)]

        return df

    def create_pokemon(
        self,
        name: str,
        pokedex_num: int,
        primary_type: str | None = None,
        color: str = "gray",
        sex: str = "male",
        level: int = 1,
    ) -> Pokemon:
        """Gets the values of a Pokémon and returns an instance of the appropriate subclass.

        Args:
            name (str): The Pokémon's name.
            pokedex_num (int): The Pokédex number.
            primary_type (str | None, optional): The primary type. Defaults to None.
            color (str, optional): The Pokémon's color. Defaults to "gray".
            sex (str, optional): The Pokémon's sex. Defaults to "male".
            level (int, optional): The Pokémon's level. Defaults to 1.

        Returns:
            Pokemon: An instance of the appropriate Pokemon subclass.
        """
        # Map type names (as they appear in the CSV) to subclass constructors
        TYPE_CLASS: dict = {
            "normal": Normal,
            "fire": Fire,
            "water": Water,
            "grass": Grass,
            "electric": Electric,
            "ice": Ice,
            "fighting": Fighting,
            "poison": Poison,
            "ground": Ground,
            "flying": Flying,
            "psychic": Psychic,
            "bug": Bug,
            "rock": Rock,
            "ghost": Ghost,
            "dragon": Dragon,
            "dark": Dark,
            "steel": Steel,
            "fairy": Fairy,
        }

        if isinstance(primary_type, str):
            primary_type = primary_type.strip()

        cls: type[Pokemon] = Pokemon
        if primary_type and primary_type in TYPE_CLASS:
            cls = TYPE_CLASS[primary_type]

        # Subclass constructors expect (name, pokedex_num, color, sex, level)
        try:
            return cls(name, pokedex_num, color, sex, level)
        except TypeError:
            # Fallback to base Pokemon if subclass constructor signature differs
            return Pokemon(name, pokedex_num, primary_type, color, sex, level)

    def choose_pokemon(self) -> list[Pokemon]:
        """Interactively choose up to 6 Pokémon for this trainer.

        Prompts the user to enter a Pokédex number and the Pokémon's type.

        Returns:
            list[Pokemon]: The list of chosen Pokémon objects.
        """
        Page = 0
        while True:
            print(
                f"{self.name}, choose Pokémon #{len(self.pokemon) + 1} for the battle."
            )
            already_chosen = [p.get_attribute("pokemon_name") for p in self.pokemon]
            df = self.pokemon_available(already_chosen)

            while True:
                try:
                    self.print_dex(Page, df)

                    vp = df[20 * Page : 20 * (Page + 1)]
                    vn = vp["pokedex_number"].tolist()

                    chosen_str = (
                        input("Enter pokedex number or (z/x to change page): ")
                        .strip()
                        .lower()
                    )

                    if chosen_str == "z":
                        Page = max(0, Page - 1)
                        continue
                    elif chosen_str == "x":
                        Page = min((len(df) - 1) // 20, Page + 1)
                        continue

                    chosen: int = int(chosen_str)
                    if chosen not in vn:
                        print("Choose a Pokémon visible on this page.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Enter a number or z/x.")

            row_df = df.loc[df["pokedex_number"] == chosen]
            if row_df.empty:
                print("Invalid number. Try again.")
                continue

            row: Series = row_df.iloc[0]
            name = row["pokemon_name"]
            pokedex_number = int(row["pokedex_number"])
            poke_type = row["type1"]

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
                self.create_pokemon(
                    name, pokedex_number, poke_type, "gray", "male", level
                )
            )
            print(f"\n {self.name} chose {name} for the battle!")

            if len(self.pokemon) == 6:
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

    def print_dex(self, page: int = 0, df: pd.DataFrame | None = None) -> None:
        """Prints the Pokédex page with available Pokémon.

        Args:
            page (int, optional): The page number to display. Defaults to 0.
            df (pd.DataFrame | None, optional): DataFrame with Pokémon data.
                Defaults to None.
        """
        if df is None:
            df = pd.read_csv(Pokemon.csv_path)
        print(f"Poke_dex - Page #{page + 1}")
        print(f"{'#':<5} {'Name':<9} {'Type':<7} {'ATK':<4} {'HP':<4}")
        for index, row in df[20 * page : 20 * (page + 1)].iterrows():
            print(
                f"{row['pokedex_number']} / {row['pokemon_name']} / {row['type1']} / {row['attack']} / {row['hp']}"
            )


class Field:
    """Manages a battle between two Trainer instances.

    Responsibilities:
    - Track each trainer's team and active Pokémon
    - Keep combat HP for each Pokémon
    - Handle turns, switches, attacks

    Attributes:
        trainer1 (Trainer): First trainer in the battle.
        trainer2 (Trainer): Second trainer in the battle.
    """

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        """Initializes the battle field.

        Args:
            trainer1 (Trainer): First trainer.
            trainer2 (Trainer): Second trainer.
        """
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.__team1 = trainer1.pokemon.copy()
        self.__team2 = trainer2.pokemon.copy()
        self.__active1 = self.__team1[0] if self.__team1 else None
        self.__active2 = self.__team2[0] if self.__team2 else None
        self.__combat_hp = {}
        self.__combat_attack = {}
        self.__combat_defense = {}
        self.__combat_sp_attack = {}
        self.__combat_sp_defense = {}
        self.__combat_speed = {}
        self.__turn_number = 0
        self.active1_moves: list[Move] = []
        self.active2_moves: list[Move] = []

        for pokemon in self.__team1:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp
            self.__combat_attack[pokemon] = pokemon.get_stats().attack
            self.__combat_defense[pokemon] = pokemon.get_stats().defense
            self.__combat_sp_attack[pokemon] = pokemon.get_stats().sp_attack
            self.__combat_sp_defense[pokemon] = pokemon.get_stats().sp_defense
            self.__combat_speed[pokemon] = pokemon.get_stats().speed

        for pokemon in self.__team2:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp
            self.__combat_attack[pokemon] = pokemon.get_stats().attack
            self.__combat_defense[pokemon] = pokemon.get_stats().defense
            self.__combat_sp_attack[pokemon] = pokemon.get_stats().sp_attack
            self.__combat_sp_defense[pokemon] = pokemon.get_stats().sp_defense
            self.__combat_speed[pokemon] = pokemon.get_stats().speed

    def get_team1(self) -> list[Pokemon]:
        return self.__team1

    def get_team2(self) -> list[Pokemon]:
        return self.__team2

    def get_active1(self) -> Pokemon | None:
        return self.__active1

    def get_active2(self) -> Pokemon | None:
        return self.__active2

    def get_turn_number(self) -> int:
        return self.__turn_number

    def get_combat_hp(self, pokemon: Pokemon) -> int:
        """Gets the current combat HP of a Pokémon.

        Args:
            pokemon (Pokemon): The Pokémon to query.

        Returns:
            int: Current HP value.
        """
        return self.__combat_hp.get(pokemon, 0)

    def set_combat_hp(self, pokemon: Pokemon, value: int) -> None:
        """Sets the combat HP of a Pokémon.

        Args:
            pokemon (Pokemon): The Pokémon to modify.
            value (int): The new HP value.
        """
        self.__combat_hp[pokemon] = max(0, value)

    def reduce_hp(self, pokemon: Pokemon, damage: int) -> None:
        """Reduces the HP of a Pokémon by a damage amount.

        Args:
            pokemon (Pokemon): The Pokémon taking damage.
            damage (int): Amount of damage to apply.
        """
        current = self.get_combat_hp(pokemon)
        self.set_combat_hp(pokemon, current - damage)

    def mod_combat_hp(self, pokemon: Pokemon, hp_: int) -> None:
        current = self.get_combat_hp(pokemon)
        self.set_combat_hp(pokemon, current + hp_)

    def get_combat_attack(self, pokemon: Pokemon) -> int:
        return self.__combat_attack.get(pokemon, 0)

    def get_combat_defense(self, pokemon: Pokemon) -> int:
        return self.__combat_defense.get(pokemon, 0)

    def get_combat_sp_attack(self, pokemon: Pokemon) -> int:
        return self.__combat_sp_attack.get(pokemon, 0)

    def get_combat_sp_defense(self, pokemon: Pokemon) -> int:
        return self.__combat_sp_defense.get(pokemon, 0)

    def get_combat_speed(self, pokemon: Pokemon) -> int:
        return self.__combat_speed.get(pokemon, 0)

    def set_combat_attack(self, pokemon: Pokemon, at_: int) -> None:
        self.__combat_attack[pokemon] = max(0, at_)

    def set_combat_defense(self, pokemon: Pokemon, def_: int) -> None:
        self.__combat_defense[pokemon] = max(0, def_)

    def set_combat_sp_attack(self, pokemon: Pokemon, sp_a: int) -> None:
        self.__combat_sp_attack[pokemon] = max(0, sp_a)

    def set_combat_sp_defense(self, pokemon: Pokemon, sp_d: int) -> None:
        self.__combat_sp_defense[pokemon] = max(0, sp_d)

    def set_combat_speed(self, pokemon: Pokemon, sp: int) -> None:
        self.__combat_speed[pokemon] = max(0, sp)

    def mod_combat_attack(self, pokemon: Pokemon, at_: int) -> None:
        current = self.get_combat_attack(pokemon)
        self.set_combat_attack(pokemon, current + at_)

    def mod_combat_defense(self, pokemon: Pokemon, def_: int) -> None:
        current = self.get_combat_defense(pokemon)
        self.set_combat_defense(pokemon, current + def_)

    def mod_combat_sp_attack(self, pokemon: Pokemon, sp_a: int) -> None:
        current = self.get_combat_sp_attack(pokemon)
        self.set_combat_sp_attack(pokemon, current + sp_a)

    def mod_combat_sp_defense(self, pokemon: Pokemon, sp_d: int) -> None:
        current = self.get_combat_sp_defense(pokemon)
        self.set_combat_sp_defense(pokemon, current + sp_d)

    def mod_combat_speed(self, pokemon: Pokemon, sp: int) -> None:
        current = self.get_combat_speed(pokemon)
        self.set_combat_speed(pokemon, current + sp)

    def end_battle(self) -> bool:
        """Checks if the battle has ended.

        Returns:
            bool: True if at least one team is completely defeated.
        """
        team1_alive = any(self.get_combat_hp(p) > 0 for p in self.__team1)
        team2_alive = any(self.get_combat_hp(p) > 0 for p in self.__team2)
        return not (team1_alive and team2_alive)

    def winner_game(self) -> Trainer | None:
        """Determines the winner of the battle.

        Returns:
            Trainer | None: The winning trainer or None if battle isn't over.
        """
        if not self.end_battle():
            return None
        team1_alive = any(self.get_combat_hp(p) > 0 for p in self.__team1)
        return self.trainer1 if team1_alive else self.trainer2

    def pokemon_available(self, trainer: Trainer) -> list[Pokemon]:
        """Gets list of Pokémon that can still battle for a trainer.

        Args:
            trainer (Trainer): The trainer to query.

        Returns:
            list[Pokemon]: List of available Pokémon.
        """
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

    def switch_defeat(self, trainer: Trainer) -> bool:
        """Checks if active Pokémon fainted and trainer has replacements.

        Args:
            trainer (Trainer): The trainer to check.

        Returns:
            bool: True if switch is needed and possible.
        """
        active = self.__active1 if trainer == self.trainer1 else self.__active2
        if active is None:
            return False
        return (
            self.get_combat_hp(active) <= 0 and len(self.pokemon_available(trainer)) > 0
        )

    def switch_pokemon(self, trainer: Trainer, new_pokemon: Pokemon) -> bool:
        """Switches active Pokémon for a trainer.

        Args:
            trainer (Trainer): The trainer switching Pokémon.
            new_pokemon (Pokemon): The new Pokémon to switch to.

        Returns:
            bool: True if switch was successful, False otherwise.
        """
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
        attacker_moves: list[Move],
        defender_moves: list[Move],
    ) -> tuple[int, bool, str]:
        """Executes an attack from attacker to defender using the specified move.

        Args:
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.
            move (Move): The move to use.
            attacker_moves (list[Move]): Moves used by the attacker so far.
            defender_moves (list[Move]): Moves used by the defender so far.

        Returns:
            tuple[int, bool, str]: A tuple containing:
                - damage (int): Damage dealt.
                - was_critical (bool): Whether it was a critical hit.
                - message (str): Description of what happened.
        """
        attacker_status = list(attacker.status.keys())[0] if attacker.status else None
        if attacker_status == "confused":
            value = random.randint(0, 100)
            if value <= 50:  # 50% of attacking himself
                defender = attacker
                defender_moves = attacker_moves
                move = Move(0, "Confused Hit", "normal", 40, 100, 10, "physical")
                print(f"{attacker._name} is confused and it is attacking itself!")
        
        engine = CombatEngine(
            attacker=attacker,
            defender=defender,
            move=move,
            attacker_moves=attacker_moves,
            defender_moves=defender_moves,
        )

        base_damage, was_critical, move_hit = engine.calculate_damage(
            self.__combat_attack,
            self.__combat_defense,
            self.__combat_sp_attack,
            self.__combat_sp_defense,
            self.__combat_speed,
        )
        if not move_hit:
            return (0, False, "The attack missed!")

        damage, message = self.move_effect(move, attacker, defender, base_damage)
        self.reduce_hp(defender, damage)
        effectiveness = defender.receive_attack(move.type)

        message += f" It dealt {damage} damage!"
        if was_critical:
            message += " A critical hit!"
        message += f" {effectiveness}"
        defender_Status = (
            list(defender.status.keys()) if defender.status is not None else None
        )
        if move.type == "fire" and defender_Status == "frozen":
            defender.status = {}
            message += f"{defender._name} is no longer frozen"
        return (damage, was_critical, message)

    def resolve_turn(self, action1: dict, action2: dict) -> tuple[bool, list[str]]:
        """Executes a turn based on both players' actions.

        If action is "surrender", the battle ends.
        If action is "switch", the active Pokémon is switched.
        If action is "attack", the active Pokémon attacks the opponent's active Pokémon.

        Args:
            action1 (dict): First trainer's action with keys like "action", "move", etc.
            action2 (dict): Second trainer's action.

        Returns:
            tuple[bool, list[str]]: A tuple containing:
                - continue_battle (bool): Whether the battle should continue.
                - messages (list[str]): List of message strings describing what happened.
        """
        active1 = self.get_active1()
        active2 = self.get_active2()

        if active1 is None or active2 is None:
            return False, ["A Pokémon is missing"]

        self.__turn_number += 1
        messages: list[str] = []

        if action1["action"] == "surrender":
            messages.append(f"{self.trainer1.name} surrendered!")
            messages.append(f"{self.trainer2.name} won the battle!")
            return (False, messages)

        if action2["action"] == "surrender":
            messages.append(f"{self.trainer2.name} surrendered!")
            messages.append(f"{self.trainer1.name} won the battle!")
            return (False, messages)

        if action1["action"] == "switch" and action2["action"] == "switch":
            active1 = action1["new_pokemon"]
            assert active1 is not None
            self.__active1 = active1
            self.active1_moves = []
            messages.append(f"{self.trainer1.name} sent out {active1._name}!")

            active2 = action2["new_pokemon"]
            assert active2 is not None
            self.__active2 = active2
            self.active2_moves = []
            messages.append(f"{self.trainer2.name} sent out {active2._name}!")
            messages.append(self.status_damage(active1))
            messages.append(self.status_damage(active2))
            return (True, messages)

        elif action1["action"] == "switch":
            active1 = action1["new_pokemon"]
            assert active1 is not None
            self.__active1 = active1
            self.active1_moves = []
            messages.append(f"{self.trainer1.name} sent out {active1._name}!")

            if action2["action"] == "attack":
                messages.append(active2.attack())
                messages.append(f"{active2._name} used {action2['move'].name}!")
                self.active2_moves.append(action2["move"])

                damage: int
                crit: bool
                msg: str

                damage, crit, msg = self.execute_attack(
                    active2,
                    active1,
                    action2["move"],
                    self.active2_moves,
                    self.active1_moves,
                )
                messages.append(msg)
                active1_Status = (
                    list(active1.status.keys())[0] if active1.status else None
                )
                if active1.status:
                    if active1_Status == "flinched":
                        del active1.status[active1_Status]
                        messages.append(
                            f"{active1._name} is no longer {active1_Status}"
                        )

            messages.append(self.status_damage(active1))
            messages.append(self.status_damage(active2))
            return (True, messages)

        elif action2["action"] == "switch":
            active2 = action2["new_pokemon"]
            assert active2 is not None
            self.__active2 = active2
            self.active2_moves = []
            messages.append(f"{self.trainer2.name} sent out {active2._name}!")

            if action1["action"] == "attack":
                messages.append(active1.attack())
                messages.append(f"{active1._name} used {action1['move'].name}!")
                self.active1_moves.append(action1["move"])
                damage, crit, msg = self.execute_attack(
                    active1,
                    active2,
                    action1["move"],
                    self.active1_moves,
                    self.active2_moves,
                )
                messages.append(msg)
                active2_Status = (
                    list(active2.status.keys())[0] if active2.status else None
                )
                if active2.status:
                    if active2_Status == "flinched":
                        del active2.status[active2_Status]
                        messages.append(
                            f"{active2._name} is no longer {active2_Status}"
                        )

            messages.append(self.status_damage(active1))
            messages.append(self.status_damage(active2))

            return (True, messages)

        if action1["action"] == "attack" and action2["action"] == "attack":
            if (
                self.get_combat_speed(active1) >= self.get_combat_speed(active2)
                or action1["move"].name == "Quick Attack"
            ):
                messages.append(f"{active1._name} is faster!")
                messages.append(active1.attack())
                messages.append(f"{active1._name} used {action1['move'].name}!")
                self.active1_moves.append(action1["move"])
                damage, crit, msg = self.execute_attack(
                    active1,
                    active2,
                    action1["move"],
                    self.active1_moves,
                    self.active2_moves,
                )
                messages.append(msg)
                messages.append(self.status_damage(active1))
                if self.get_combat_hp(active2) > 0:
                    messages.append(active2.attack())
                    messages.append(f"{active2._name} used {action2['move'].name}!")
                    self.active2_moves.append(action2["move"])
                    damage, crit, msg = self.execute_attack(
                        active2,
                        active1,
                        action2["move"],
                        self.active2_moves,
                        self.active1_moves,
                    )
                    messages.append(msg)
                    messages.append(self.status_damage(active2))
                    active1_Status = (
                        list(active1.status.keys())[0] if active1.status else None
                    )
                    if active1.status:
                        if active1_Status == "flinched":
                            del active1.status[active1_Status]
                            messages.append(
                                f"{active1._name} is no longer {active1_Status}"
                            )
            else:
                messages.append(f"{active2._name} is faster!")
                messages.append(active2.attack())
                messages.append(f"{active2._name} used {action2['move'].name}!")
                self.active2_moves.append(action2["move"])
                damage, crit, msg = self.execute_attack(
                    active2,
                    active1,
                    action2["move"],
                    self.active2_moves,
                    self.active1_moves,
                )
                messages.append(msg)
                messages.append(self.status_damage(active2))
                if self.get_combat_hp(active1) > 0:
                    messages.append(active1.attack())
                    messages.append(f"{active1._name} used {action1['move'].name}!")
                    self.active1_moves.append(action1["move"])
                    damage, crit, msg = self.execute_attack(
                        active1,
                        active2,
                        action1["move"],
                        self.active1_moves,
                        self.active2_moves,
                    )
                    messages.append(msg)
                    messages.append(self.status_damage(active1))
                    active2_Status = (
                        list(active2.status.keys())[0] if active2.status else None
                    )
                    if active2.status:
                        if active2_Status == "flinched":
                            del active2.status[active2_Status]
                            messages.append(
                                f"{active2._name} is no longer {active2_Status}"
                            )

            return (True, messages)

        return (True, messages)

    def remove_defeated_pokemon(self) -> tuple[bool, bool, list[str]]:
        """Checks for defeated Pokémon and removes them from teams.

        Returns:
            tuple[bool, bool, list[str]]: A tuple containing:
                - needs_switch1 (bool): Whether trainer 1 needs to switch.
                - needs_switch2 (bool): Whether trainer 2 needs to switch.
                - messages (list[str]): Messages about defeated Pokémon.
        """
        messages: list[str] = []
        needs_switch1: bool = False
        needs_switch2: bool = False

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

    def health_bar(self, current_hp: int, max_hp: int, bar_length: int = 20) -> str:
        """Returns a simple text health bar representation.

        Args:
            current_hp (int): Current HP value.
            max_hp (int): Maximum HP value.
            bar_length (int, optional): Length of the bar in characters. Defaults to 20.

        Returns:
            str: A formatted health bar string.
        """
        if max_hp <= 0:
            bar = "░" * bar_length
            return f"[{bar}] 0/0 HP"
        filled = int((current_hp / max_hp) * bar_length)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty

        return f"[{bar}] {current_hp}/{max_hp} HP"

    def move_effect(
        self, move: Move, attacker: Pokemon, defender: Pokemon, damage: int
    ) -> tuple[int, str]:
        """Applies secondary effects of the move, if any.

        This method checks if the move has any secondary effects (like
        status conditions or stat changes) and applies them to the
        attacker or defender as appropriate.

        Args:
            move (Move): The move being used.
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.
            damage (int): Base damage before effects.

        Returns:
            tuple[int, str]: A tuple containing:
                - final_damage (int): Damage after applying effects.
                - message (str): Description of effects applied.
        """
        hits: int = 1  # Default number of hits is 1
        message: str = ""

        if (
            move.name == "Absorb"
            or move.name == "Leech Life"
            or move.name == "Mega Drain"
        ):
            heal_amount = math.floor(damage / 2)
            self.mod_combat_hp(attacker, heal_amount)
            message = f"{attacker._name} healed for {heal_amount} HP!"

        if move.name == "Acid":
            random_value: int = random.randint(1, 100)
            if random_value <= 10:  # 10% chance to lower defense
                self.mod_combat_defense(defender, -1)
                message = f"{defender._name}'s Defense fell!"

        if move.name == "Acid Armor" or move.name == "Barrier":
            self.mod_combat_defense(attacker, 2)
            message = f"{attacker._name}'s Defense rose sharply!"
        if move.name == "Agility":
            self.mod_combat_speed(attacker, 2)
            message = f"{attacker._name}'s Speed rose sharply!"

        if move.name == "Amnesia" or move.name == "Growth":
            self.mod_combat_sp_attack(attacker, 2)
            self.mod_combat_sp_defense(attacker, 2)
            message = f"{attacker._name}'s Special rose sharply!"

        if move.name == "Aurora Beam":
            random_value = random.randint(1, 100)
            if random_value <= 10:  # 10% chance to lower attack
                self.mod_combat_attack(defender, -1)
                message = f"{defender._name}'s Attack fell!"

        if (
            move.name == "Barrage"
            or move.name == "Comet Punch"
            or move.name == "Double Slap"
            or move.name == "Fury Attack"
            or move.name == "Fury Swipes"
            or move.name == "Pin Missile"
            or move.name == "Spike Cannon"
        ):
            random_value = random.randint(1, 100)
            if random_value <= 37:  # 37% chance to hit 2 times
                hits = 2
            if 37 < random_value < 75:  # 37% chance to hit 3 times
                hits = 3
            if 75 <= random_value <= 87:  # 12% chance to hit 4 times
                hits = 4
            if random_value > 87:  # 13% chance to hit 5 times
                hits = 5
            message = f"{attacker._name} will hit {hits} times!"

        if move.name == "Bite" or move.name == "Bone Club" or move.name == "Hyper Fang":
            random_value = random.randint(1, 100)
            if random_value <= 10 and (
                defender.status is None or defender.status == {}
            ):  # 10% chance to flinch
                defender.apply_status("flinched")
                message = f"{defender._name} flinched!"

        if (
            move.name == "Blizzard"
            or move.name == "Ice Beam"
            or move.name == "Ice Punch"
        ):
            random_value = random.randint(1, 100)
            if (
                random_value <= 10
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") != "ice"
            ):  # 10% chance to freeze
                defender.apply_status("frozen")
                message = f"{defender._name} was frozen!"

        if move.name == "Body Slam" or move.name == "Lick":
            random_value = random.randint(1, 100)
            if random_value <= 30 and (
                defender.status is None or defender.status == {}
            ):  # 30% chance to paralyze
                defender.apply_status("paralyzed")
                message = f"{defender._name} was paralyzed!"

        if move.name == "Bonemerang" or move.name == "Double Kick":
            hits = 2
            message = f"{attacker._name} will hit {hits} times!"
        if move.name == "Bubble" or move.name == "Constrict":
            random_value = random.randint(1, 100)
            if random_value <= 10:  # 10% chance to lower speed
                self.mod_combat_speed(defender, -1)
                message = f"{defender._name}'s Speed fell!"

        if move.name == "Bubble Beam":
            random_value = random.randint(1, 100)
            if random_value <= 33:  # 33% chance to lower speed
                self.mod_combat_speed(defender, -1)
                message = f"{defender._name}'s Speed fell!"

        if move.name == "Confuse Ray" or move.name == "Supersonic":
            if defender.status is None or defender.status == {}:
                defender.apply_status("confused")
                message = f"{defender._name} became confused!"

        if move.name == "Confusion" or move.name == "Psybeam":
            random_value = random.randint(1, 100)
            if random_value <= 10 and (
                defender.status is None or defender.status == {}
            ):  # 10% chance to confuse
                defender.apply_status("confused")
                message = f"{defender._name} became confused!"

        if move.name == "Defense Curl" or move.name == "Harden":
            self.mod_combat_defense(attacker, 1)
            message = f"{attacker._name}'s Defense rose!"
        if move.name == "Dizzy Punch":
            random_value = random.randint(1, 100)
            if random_value <= 20 and (
                defender.status is None or defender.status == {}
            ):  # 20% chance to confuse
                defender.apply_status("confused")
                message = f"{defender._name} became confused!"

        if move.name == "Double-Edge":
            recoil = math.floor(damage / 4)
            self.reduce_hp(attacker, recoil)
            message = f"{attacker._name} took {recoil} recoil damage!"

        if move.name == "Dream Eater":
            if defender.status == "asleep":
                heal_amount = math.floor(damage / 2)
                self.mod_combat_hp(attacker, heal_amount)
                message = f"{attacker._name} healed for {heal_amount} HP!"

        if (
            move.name == "Fissure"
            or move.name == "Guillotine"
            or move.name == "Horn Drill"
        ):
            if self.get_combat_speed(attacker) > self.get_combat_speed(defender):
                random_value = random.randint(1, 100)
                if random_value <= 30:  # 30% chance to instantly defeat
                    damage = self.get_combat_hp(defender)
                    message = f"{defender._name} was instantly defeated!"

        if move.name == "Flamethrower" or move.name == "Ember":
            random_value = random.randint(1, 100)
            if (
                random_value <= 10
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") != "fire"
            ):  # 10% chance to burn
                defender.apply_status("burned")
                message = f"{defender._name} was burned!"

        if (
            move.name == "Glare"
            or move.name == "Stun Spore"
            or move.name == "Thunder Wave"
        ):
            if (
                defender.status is None or defender.status == {}
            ) and defender.get_attribute("type") != "ground":
                defender.apply_status("paralyzed")
                message = f"{defender._name} was paralyzed!"

        if move.name == "Growl":
            self.mod_combat_attack(defender, -1)
            message = f"{defender._name}'s Attack fell!"

        if move.name == "Haze":
            self.__combat_attack[attacker] = attacker.get_stats().attack
            self.__combat_defense[attacker] = attacker.get_stats().defense
            self.__combat_sp_attack[attacker] = attacker.get_stats().sp_attack
            self.__combat_sp_defense[attacker] = attacker.get_stats().sp_defense
            self.__combat_speed[attacker] = attacker.get_stats().speed

            self.__combat_attack[defender] = defender.get_stats().attack
            self.__combat_defense[defender] = defender.get_stats().defense
            self.__combat_sp_attack[defender] = defender.get_stats().sp_attack
            self.__combat_sp_defense[defender] = defender.get_stats().sp_defense
            self.__combat_speed[defender] = defender.get_stats().speed
            message = (
                f"{attacker._name} and {defender._name}'s stat changes were reset!"
            )

            self.active1_moves = []
            self.active2_moves = []
            attacker_status = (
                list(attacker.status.keys())[0] if attacker.status else None
            )
            if attacker_status:
                if attacker_status == "confused":
                    attacker.status = {}
                    message = f"{attacker._name} is no longer confused!"
            defender_status = (
                list(defender.status.keys())[0] if defender.status else None
            )
            if defender_status:
                if defender_status in [
                    "confused",
                    "flinched",
                    "paralyzed",
                    "frozen",
                    "burned",
                    "asleep",
                    "poisoned",
                ]:
                    defender.status = None
                    message = (
                        f"{defender._name} is no longer affected by status conditions!"
                    )

        if (
            move.name == "Headbutt"
            or move.name == "Low Kick"
            or move.name == "Rolling Kick"
            or move.name == "Stomp"
        ):
            random_value = random.randint(1, 100)
            if random_value <= 30 and (
                defender.status is None or defender.status == {}
            ):  # 30% chance to flinch
                defender.apply_status("flinched")
                message = f"{defender._name} flinched!"

        if (
            move.name == "Hypnosis"
            or move.name == "Lovely Kiss"
            or move.name == "Sing"
            or move.name == "Sleep Powder"
            or move.name == "Spore"
        ):
            if defender.status is None or defender.status == {}:
                defender.apply_status("asleep")
                message = f"{defender._name} fell asleep!"

        if move.name == "Leech Seed":
            if (
                defender.status is None or defender.status == {}
            ) and defender.get_attribute("type") != "grass":
                defender.apply_status("seeded")
                message = f"{defender._name} was seeded!"

        if move.name == "Leer" or move.name == "Tail Whip":
            self.mod_combat_defense(defender, -1)
            message = f"{defender._name}'s Defense fell!"

        if move.name == "Meditate":
            self.mod_combat_attack(attacker, 1)
            message = f"{attacker._name}'s Attack rose!"
        if move.name == "Metronome":
            while True:
                random_move = random.choice(
                    [
                        move
                        for poke in [attacker, defender]
                        for move in poke.get_moveset().current_moves
                    ]
                )
                if random_move.name != "Metronome" and random_move.name != "Struggle":
                    break
            message = f"{attacker._name} used Metronome and called {random_move.name}!"
            damage, was_critical, msg = self.execute_attack(
                attacker,
                defender,
                random_move,
                self.active1_moves
                if attacker == self.__active1
                else self.active2_moves,
                self.active2_moves
                if defender == self.__active2
                else self.active1_moves,
            )

        if move.name == "Mimic":
            for moves in defender.get_moveset().current_moves:
                print(moves.name)
            while True:
                try:
                    choice = str(
                        input(
                            f"Write the name of the move from {defender._name}'s moveset: "
                        )
                    ).capitalize()
                    break
                except ValueError:
                    print("Unvalid input, try again")
            for moves in defender.get_moveset().current_moves:
                if moves.name.lower() == choice.lower():
                    damage, was_critical, msg = self.execute_attack(
                        attacker,
                        defender,
                        moves,
                        self.active1_moves
                        if attacker == self.__active1
                        else self.active2_moves,
                        self.active2_moves
                        if defender == self.__active2
                        else self.active1_moves,
                    )
                    message = msg
                    break

        if move.name == "Mirror Move":
            if self.active2_moves:
                last_move = (
                    self.active2_moves[-1]
                    if attacker == self.__active1
                    else self.active1_moves[-1]
                )
                message = (
                    f"{attacker._name} used Mirror Move and copied {last_move.name}!"
                )
                damage, was_critical, msg = self.execute_attack(
                    attacker,
                    defender,
                    last_move,
                    self.active1_moves
                    if attacker == self.__active1
                    else self.active2_moves,
                    self.active2_moves
                    if defender == self.__active2
                    else self.active1_moves,
                )
                message += msg
            else:
                message = "Rival has not used any move"

        if move.name == "Night Shade" or move.name == "Seismic Toss":
            level = attacker.get_attribute("level")
            damage = level

        if (
            move.name == "Poison Gas"
            or move.name == "Poison Powder"
            or move.name == "Toxic"
        ):
            if (
                defender.status is None or defender.status == {}
            ) and defender.get_attribute("type") not in ["poison", "steel"]:
                defender.apply_status("poisoned")
                message = f"{defender._name} was poisoned!"

        if move.name == "Poison Sting":
            random_value = random.randint(1, 100)
            if (
                random_value <= 20
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") not in ["poison", "steel"]
            ):  # 20% chance to poison
                defender.apply_status("poisoned")
                message = f"{defender._name} was poisoned!"

        if move.name == "Psychic":
            random_value = random.randint(1, 100)
            if random_value <= 33:  # 33% chance to lower sp_defense
                self.mod_combat_sp_defense(defender, -1)
                self.mod_combat_sp_attack(defender, -1)
                message = f"{defender._name}'s Special fell!"

        if move.name == "Psywave":
            level = attacker.get_attribute("level")
            random_multiplier = random.uniform(0.5, 1.5)
            damage = math.floor(level * random_multiplier)
            message = f"{defender._name} took {damage} damage from Psywave!"

        if move.name == "Recover" or move.name == "Soft-Boiled":
            heal_amount = math.floor(attacker.get_stats().hp / 2)
            self.mod_combat_hp(attacker, heal_amount)
            message = f"{attacker._name} healed for {heal_amount} HP!"

        if move.name == "Rest":
            attacker.status = None
            attacker.apply_status("asleep")
            self.set_combat_hp(attacker, attacker.get_stats().hp)
            message = f"{attacker._name} restored its HP and fell asleep!"

        if move.name == "Screech":
            self.mod_combat_defense(defender, -2)
            message = f"{defender._name}'s Defense fell sharply!"

        if move.name == "Self-Destruct" or move.name == "Explosion":
            self.set_combat_hp(attacker, 0)
            message = f"{attacker._name} fainted due to recoil!"

        if move.name == "Sharpen":
            self.mod_combat_attack(attacker, 1)
            message = f"{attacker._name}'s Attack rose!"

        if move.name == "Sludge":
            random_value = random.randint(1, 100)
            if (
                random_value <= 30
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") not in ["poison", "steel"]
            ):  # 30% chance to poison
                defender.apply_status("poisoned")
                message = f"{defender._name} was poisoned!"

        if move.name == "Smog":
            random_value = random.randint(1, 100)
            if (
                random_value <= 40
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") not in ["Poison", "Steel"]
            ):  # 40% chance to poison
                defender.apply_status("Poisoned")
                message = f"{defender._name} was poisoned!"

        if move.name == "Splash":
            message = f"{attacker._name} splashed around but nothing happened!"

        if move.name == "String Shot":
            self.mod_combat_speed(defender, -1)
            message = f"{defender._name}'s Speed fell!"
        if move.name == "Struggle":
            recoil = math.floor(damage / 2)
            self.reduce_hp(attacker, recoil)
            message = f"{attacker._name} took {recoil} recoil damage!"

        if move.name == "Submission" or move.name == "Take Down":
            recoil = math.floor(damage / 4)
            self.reduce_hp(attacker, recoil)
            message = f"{attacker._name} took {recoil} recoil damage!"

        if move.name == "Substitute":
            heal_amount = math.floor(attacker.get_stats().hp / 4)
            self.mod_combat_hp(attacker, heal_amount)
            message = f"{attacker._name} created a substitute that can absorb {heal_amount} HP worth of damage!"

        if move.name == "Super Fang":
            current_hp = self.get_combat_hp(defender)
            damage = math.floor(current_hp / 2)
            message = f"{defender._name} took {damage} damage from Super Fang!"
        if move.name == "Sword Dance":
            self.mod_combat_attack(attacker, 2)
            message = f"{attacker._name}'s Attack rose sharply!"

        if move.name == "Transform":
            attacker.set_type(defender.get_attribute("type"))

            # Copy enemy´s stats
            self.__combat_attack[attacker] = self.__combat_attack[defender]
            self.__combat_defense[attacker] = self.__combat_defense[defender]
            self.__combat_sp_attack[attacker] = self.__combat_sp_attack[defender]
            self.__combat_sp_defense[attacker] = self.__combat_sp_defense[defender]
            self.__combat_speed[attacker] = self.__combat_speed[defender]

            # Copy enemy´s movements
            new_moves = []
            for mv in defender.get_moveset().current_moves:
                new_mv = Move(
                    mv.id,
                    mv.name,
                    mv.type,
                    mv.power,
                    mv.accuracy,
                    mv.pp,  # actual PP´s
                    mv.category,
                )
                new_moves.append(new_mv)

            attacker._moveset.current_moves = new_moves

            # Copy enemy´s weaknesses/resistances/immunities
            attacker._weaknesses = defender._weaknesses.copy()
            attacker._resistances = defender._resistances.copy()
            attacker._immunities = defender._immunities.copy()

            message = f"{attacker._name} transformed into {defender._name}!"
            return 0, message

        if (
            move.name == "Thunder"
            or move.name == "Thunderbolt"
            or move.name == "Thunder Punch"
            or move.name == "Thunder Shock"
        ):
            random_value = random.randint(1, 100)
            if (
                random_value <= 10
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") != "electric"
            ):  # 10% chance to paralyze
                defender.apply_status("paralyzed")
                message = f"{defender._name} was paralyzed!"

        if move.name == "Twineedle":
            hits = 2
            message = f"{attacker._name} will hit {hits} times!"
            random_value = random.randint(1, 100)
            if (
                random_value <= 20
                and (defender.status is None or defender.status == {})
                and defender.get_attribute("type") not in ["poison", "steel"]
            ):  # 20% chance to poison
                defender.apply_status("poisoned")
                message = f"{defender._name} was poisoned!"

        if move.name == "Withdraw":
            self.mod_combat_defense(attacker, 1)
            message = f"{attacker._name}'s Defense rose!"

        return hits * damage, message

    def status_damage(self, attacker: Pokemon) -> str:
        """Applies damage from status conditions like burn or poison.

        Args:
            attacker (Pokemon): The Pokémon to check for status damage.

        Returns:
            str: Message describing status damage if any occurred.
        """
        message = ""
        poke_status = list(attacker.status.keys())[0] if attacker.status else None
        if poke_status:
            if (
                poke_status == "burned"
                or poke_status == "poisoned"
                or poke_status == "seeded"
            ):
                damage = math.floor((attacker.get_stats().hp) / 16)
                message = f"{attacker._name} took {damage} damage from {poke_status}"
                self.reduce_hp(attacker, damage)
        return message


class Battle:
    """Handles all interactions for battles.

    Responsibilities:
    - Display battle and turn headers
    - Show battle status
    - Prompt trainers for actions
    - Display messages
    - Manage the battle loop

    Attributes:
        field (Field): The battle field being managed.
    """

    def __init__(self, field: Field) -> None:
        """Initializes the Battle interface.

        Args:
            field (Field): The field where the battle takes place.
        """
        self.field = field

    def display_battle_header(self) -> None:
        """Display the battle header"""
        print(60 * "=")
        print(f"{self.field.trainer1.name} VS {self.field.trainer2.name}")
        print(60 * "=")

    def display_turn_header(self) -> None:
        """Display the turn header"""
        print("\n" + 60 * "=")
        print(f"TURN #{self.field.get_turn_number() + 1}")
        print(60 * "=")

    def display_battle_status(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ) -> None:
        """Displays the current battle status.

        Args:
            trainer (Trainer): The trainer whose turn it is.
            active_pokemon (Pokemon): The active Pokémon.
            enemy_pokemon (Pokemon): The enemy Pokémon.
        """
        active_hp = self.field.get_combat_hp(active_pokemon)
        enemy_hp = self.field.get_combat_hp(enemy_pokemon)
        active_status = (
            ", ".join(active_pokemon.status.keys())
            if active_pokemon.status
            else "Normal"
        )
        enemy_status = (
            ", ".join(enemy_pokemon.status.keys()) if enemy_pokemon.status else "Normal"
        )

        print(f"""
        {50 * "="}
        Turn: {trainer.name}
        {active_pokemon._name:<20} VS {enemy_pokemon._name:>20}
        {self.field.health_bar(active_hp, active_pokemon._stats.hp)}  {self.field.health_bar(enemy_hp, enemy_pokemon._stats.hp)}
        Current Status:{active_status.capitalize()}                 Current Status: {enemy_status.capitalize()}
        {50 * "="}
        """)

    def action_py(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ) -> dict:
        """Prompts the trainer for an action during their turn.

        Args:
            trainer (Trainer): The trainer making the decision.
            active_pokemon (Pokemon): The trainer's active Pokémon.
            enemy_pokemon (Pokemon): The opponent's active Pokémon.

        Returns:
            dict: A dictionary describing the chosen action.
        """
        self.display_battle_status(trainer, active_pokemon, enemy_pokemon)

        choice = input("""
              (1) Attack
              (2) Switch Pokémon
              (0) Surrender
              """)

        if choice == "1":
            return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
        elif choice == "2":
            return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
        elif choice == "0":
            return self.choice_surrender(trainer)
        else:
            print("Invalid choice. Try again.")
            return self.action_py(trainer, active_pokemon, enemy_pokemon)

    def choice_attack(
        self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon
    ) -> dict:
        """Prompts the trainer to choose an attack move.

        Args:
            trainer (Trainer): The trainer choosing.
            active_pokemon (Pokemon): The trainer's active Pokémon.
            enemy_pokemon (Pokemon): The opponent's active Pokémon.

        Returns:
            dict: Dictionary with "action": "attack" and "move": chosen_move.
        """
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
                chosen_move = moves[int(choice_move) - 1]
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
    ) -> dict:
        """Prompts the trainer to choose a Pokémon to switch to.

        Args:
            trainer (Trainer): The trainer choosing.
            active_pokemon (Pokemon): The trainer's current active Pokémon.
            enemy_pokemon (Pokemon): The opponent's active Pokémon.

        Returns:
            dict: Dictionary with "action": "switch" and "new_pokemon": chosen_pokemon.
        """
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
                status = (
                    ", ".join(pokemon.status.keys())
                    if isinstance(pokemon.status, dict) and pokemon.status
                    else "Normal"
                )

            print(f"({i}) {pokemon._name} {hp_bar} Status:{status}")
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

    def choice_surrender(self, trainer: Trainer) -> dict:
        """Prompts the trainer to confirm surrendering.

        Args:
            trainer (Trainer): The trainer considering surrender.

        Returns:
            dict: Dictionary with "action": "surrender" if confirmed.
        """
        confirm = input(f"Are you sure you want to surrender, {trainer.name}? (y/n) ")
        if confirm.lower() == "y":
            return {"action": "surrender"}
        else:
            print("Surrender cancelled.")
            active = (
                self.field.get_active1()
                if trainer == self.field.trainer1
                else self.field.get_active2()
            )
            enemy = (
                self.field.get_active2()
                if trainer == self.field.trainer1
                else self.field.get_active1()
            )

            assert active is not None and enemy is not None

            return self.action_py(trainer, active, enemy)

    def switch_after_defeat(self, trainer: Trainer):
        """Prompts the trainer to choose their next Pokémon after one is defeated.

        Args:
            trainer (Trainer): The trainer who needs to switch.

        Returns:
            Pokemon: The newly selected Pokémon.
        """
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

    def display_messages(self, messages: list[str]) -> None:
        """Displays a list of messages to the console.

        Args:
            messages (list[str]): Messages to display.
        """
        for msg in messages:
            print(msg)

    def battle(self) -> None:
        """Main battle loop"""
        self.display_battle_header()
        while not self.field.end_battle():
            active1 = self.field.get_active1()
            active2 = self.field.get_active2()

            if active1 is None or active2 is None:
                print("Error: missing active Pokémon.")
                break

            self.display_turn_header()

            action1 = self.action_py(self.field.trainer1, active1, active2)

            action2 = self.action_py(self.field.trainer2, active2, active1)

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
            print(f"{winner.name} is the winner!")

    def main_menu(self) -> None:
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
