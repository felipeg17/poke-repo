import pandas as pd
import random as random
from pathlib import Path

import csv


"""Class that brings the information of types.csv
and replace the classes of types of pokemon """


class TypeRelations:
    def __init__(self, filename="types.csv"):
        self._type_data = {}
        self.load_from_csv(filename)

    def load_from_csv(self, filename):
        try:
            with open(filename, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(
                    csvfile
                )  # This converts each row of the CSV into a dictionary
                for row in reader:
                    type_key = row["type"].strip().lower()

                    self._type_data[type_key] = {
                        "weak": [
                            x.strip().lower() for x in row["weaknesses"].split(";")
                        ]
                        if row["weaknesses"].strip()
                        else [],
                        "resist": [
                            x.strip().lower() for x in row["resistances"].split(";")
                        ]
                        if row["resistances"].strip()
                        else [],
                        "immune": [
                            x.strip().lower() for x in row["immunities"].split(";")
                        ]
                        if row["immunities"].strip()
                        else [],
                    }
        except FileNotFoundError:
            print(f"Error: Could not find file {filename}")
        except Exception as e:
            print(f"Error loading CSV file: {e}")

    """These functions help for getting specific parts of the structure"""

    def get_relations(self, pkm_type):
        return self._type_data.get(
            pkm_type.lower(), {"weak": [], "resist": [], "immune": []}
        )

    def get_weaknesses(self, pkm_type):
        return self.get_relations(pkm_type)["weak"]

    def get_resistances(self, pkm_type):
        return self.get_relations(pkm_type)["resist"]

    def get_immunities(self, pkm_type):
        return self.get_relations(pkm_type)["immune"]


class Pokemon:
    current_dir = Path(__file__).parent
    ### TODO: Move to another module
    # If moved, uses import from that module
    csv_path = current_dir / "utils" / "First151Pokemons.csv"
    definition = """
    Pocket Monster
    """
    _type_relations = TypeRelations(str(Path(__file__).parent / "utils" / "types.csv"))

    def __init__(
        self,
        pokemon_name: str,
        pokedex_num: int,
        type: str,
        color: str,
        sex: str | int,
        level: int = 1,
    ) -> None:
        """
        Creates a basic pokemon

        Args:
            name (int): Pokemon's name in lowercase
            pokedex_num (int): Number in the national pokedex
            type (str): Main type of the pokemon
        Returns:
           A string representation of the Pokemon.

        Raises:
            ...
        """
        # * Changed to protected so that subclasses can access them
        self._name = pokemon_name
        self._pokedex_num = pokedex_num
        self._main_type = type.lower()
        self._sex = sex
        self._color = color
        self._level = level if level >= 1 and level <= 100 else 1
        # Always creating base stats
        self._stats = Stats(
            csv_path=str(Pokemon.csv_path),
            pokedex_num=pokedex_num,
            initial_level=self._level,
        )
        # Moveset managed by another class
        self._moveset = Moveset(pokedex_num=self._pokedex_num, level=self._level)

        self._weaknesses = Pokemon._type_relations.get_weaknesses(self._main_type)
        self._resistances = Pokemon._type_relations.get_resistances(self._main_type)
        self._immunities = Pokemon._type_relations.get_immunities(self._main_type)

        self.status: dict | None = (
            None  # Status condition (e.g., 'paralyzed', 'burned')
        )

        ### TODO: Moveset
        # Shoudl be managed by another class -> composition
        # Because a pokemon HAS a moveset
        # This is a tricky one, moveset depends on level, type and pokemon
        # One approach is having a table with all moves and their characteristics
        # Then, based on level and type, assign a moveset to the pokemon
        # It implies join tables
        # Table: Moves | id | name | type | power | accuracy | pp |
        # Table: Pokemon_Moves | pokemon_id | move_id | level_learned |
        # So joining these tables and return all moves that the pokemon can learn
        # Then, select up to 4 moves based on level
        #! A pokemon can have up to 4 moves

    def level_up(self):
        # * Add docstring
        if self._level < 100:
            self._level += 1
            #! refer to: https://m.bulbapedia.bulbagarden.net/wiki/Stat
            self._stats.hp = round(self._stats.hp + (110 + self._stats.base_hp) / 100)
            self._stats.attack = round(
                self._stats.attack + (5 + self._stats.base_attack) / 100
            )
            self._stats.defense = round(
                self._stats.defense + (5 + self._stats.base_defense) / 100
            )
            self._stats.sp_attack = round(
                self._stats.sp_attack + (5 + self._stats.base_sp_attack) / 100
            )
            self._stats.sp_defense = round(
                self._stats.sp_defense + (5 + self._stats.base_sp_defense) / 100
            )
            self._stats.speed = round(
                self._stats.speed + (5 + self._stats.base_speed) / 100
            )
            print(f"{self._name} leveled up to level {self._level}!")
        else:
            print(f"{self._name} is already max level!")

    def attack(self) -> str:
        ### TODO: Return necessary information to compute attack
        return f"{self._name} is attacking!"

    def receive_attack(self, attack_type):
        ### TODO: Return necessary information to compute damage

        attack = attack_type.strip().lower()
        weaknesses = self._type_relations.get_weaknesses(self._main_type)
        resistances = self._type_relations.get_resistances(self._main_type)
        immunities = self._type_relations.get_immunities(self._main_type)

        if attack in immunities:
            return "It's immune!"
        elif attack in weaknesses:
            return "It's super effective!"
        elif attack in resistances:
            return "It's not very effective..."
        else:
            return "It's effective."

    """This is the base of STAB logic"""

    def apply_stab(self, base_power: float, move_type: str) -> float:
        if move_type.lower() == self._main_type.lower():
            return base_power * 1.5
        return base_power

    def update_stats_after_battle(self):
        ### TODO: Update stats based on battle outcomes
        pass

    def get_stats(self):
        return self._stats

    def get_attribute(self, attribute_name: str):
        # Dictionary mapping public names to protected attributes
        attribute_map = {
            "pokemon_name": self._name,
            "pokedex_num": self._pokedex_num,
            "type": self._main_type,
            "color": self._color,
            "sex": self._sex,
            "level": self._level,
            "stats": self._stats,
            "weaknesses": self._weaknesses,
            "resistances": self._resistances,
            "immunities": self._immunities,
        }

        if attribute_name in attribute_map:
            return attribute_map.get(attribute_name)
        else:
            raise AttributeError(f"Pokemon has no attribute '{attribute_name}'")
        # Module for evolutions

    def set_type(self, type: str):
        self._main_type = type

    def __str__(self):
        return (
            f"{self._name} (#{self._pokedex_num}) - "
            f"Type: {self._main_type}, Level: {self._level} "
            f"- {self.evolution_hint()}"
        )

    def _get_row(self):
        df = pd.read_csv(Pokemon.csv_path)
        row = df.loc[df["pokedex_number"] == self._pokedex_num].iloc[0]
        return row

    def can_evolve(self, item=None, trade: bool = False) -> bool:
        row = self._get_row()
        evo_level = int(row.get("evolution_level", 0))
        by_stone = int(row.get("evolves_by_stone", 0)) == 1
        by_trade = int(row.get("evolves_by_trade", 0)) == 1
        if by_trade and (trade or (isinstance(item, str) and item.lower() == "trade")):
            return True
        if by_stone and item:
            return True
        if evo_level > 0 and self._level >= evo_level:
            return True
        return False

    def _get_evolved_form_pokedex_num(self) -> int:
        """
        Determines the Pokedex number of the evolved form.
        For sequential evolutions (like Bulbasaur->Ivysaur), it's typically +1.
        Returns 0 if Pokemon cannot evolve.
        """
        # Simple evolution mapping - in most cases, evolved form is next pokedex number
        # For Pokemon in evolution chains, this works for Gen 1
        row = self._get_row()
        evolves_once = int(row.get("evolves_once", 0)) == 1
        evolves_twice = int(row.get("evolves_twice", 0)) == 1

        if evolves_once or evolves_twice:
            # For most Gen 1 Pokemon, evolution is just +1 Pokedex number
            return self._pokedex_num + 1
        return 0

    def evolve(self, item=None, trade: bool = False) -> bool:
        """
        Evolves the Pokemon if conditions are met.
        This transforms the Pokemon: updates name, pokedex_num, and recalculates stats for current level.
        """
        if not self.can_evolve(item=item, trade=trade):
            print(f"{self._name.capitalize()} no puede evolucionar aún.")
            return False

        row = self._get_row()
        evo_level = int(row.get("evolution_level", 0))
        by_stone = int(row.get("evolves_by_stone", 0)) == 1
        by_trade = int(row.get("evolves_by_trade", 0)) == 1

        # Get the evolved form's pokedex number
        evolved_pokedex_num = self._get_evolved_form_pokedex_num()
        if evolved_pokedex_num == 0:
            print(f"{self._name.capitalize()} no puede evolucionar aún.")
            return False

        # Get evolved form data
        df = pd.read_csv(Pokemon.csv_path)
        evolved_row = df.loc[df["pokedex_number"] == evolved_pokedex_num].iloc[0]
        evolved_name = evolved_row["pokemon_name"]

        old_name = self._name

        # Print evolution message
        if by_trade and (trade or (isinstance(item, str) and item.lower() == "trade")):
            print(f"¡{old_name.capitalize()} está evolucionando por intercambio!")
        elif by_stone and item:
            print(f"¡{old_name.capitalize()} está evolucionando con {item}!")
        elif evo_level > 0 and self._level >= evo_level:
            print(
                f"¡{old_name.capitalize()} está evolucionando al nivel {self._level}!"
            )

        # Transform the Pokemon
        self._name = evolved_name.lower()
        self._pokedex_num = evolved_pokedex_num

        # Recalculate stats for the evolved form at current level
        self._stats = Stats(
            csv_path=str(Pokemon.csv_path),
            pokedex_num=self._pokedex_num,
            initial_level=self._level,
        )

        print(
            f"¡Felicidades! {old_name.capitalize()} evolucionó a {self._name.capitalize()}!"
        )
        return True

    def evolution_hint(self) -> str:
        row = self._get_row()
        evo_level = int(row.get("evolution_level", 0))
        by_stone = int(row.get("evolves_by_stone", 0)) == 1
        by_trade = int(row.get("evolves_by_trade", 0)) == 1
        if by_trade:
            return "Evoluciona por intercambio (nivel de referencia 45)."
        if by_stone:
            return "Evoluciona por piedra."
        if evo_level > 0:
            return f"Evoluciona al nivel {evo_level}."
        return "No evoluciona."

    def get_moveset(self):
        return self._moveset

    def set_moveset(self, new_moveset: "Moveset"):
        self._moveset = new_moveset

    def show_moves(self):
        self._moveset.show_moves()

    def apply_status(self, new_status: str):
        if self.status is None:
            self.status = {}  # inicializar si está vacío
        if new_status == "paralyzed":
            turns_left = 999
        elif new_status == "burned":
            turns_left = 999
        elif new_status == "poisoned":
            turns_left = 999
        elif new_status == "asleep":
            turns_left = random.randint(1, 3)
        elif new_status == "frozen":
            turns_left = 999
        elif new_status == "confused":
            turns_left = 999
        elif new_status == "seeded":
            turns_left = 999
        elif new_status == "flinched":
            turns_left = 1
        else:
            # Unknown status, do not apply
            return
        self.status[new_status] = turns_left


### TODO: Move to another module
class Stats:
    def __init__(self, csv_path: str, pokedex_num: int, initial_level: int = 1):
        df = pd.read_csv(csv_path)
        row = df.loc[df["pokedex_number"] == pokedex_num]
        self.initial_level = initial_level
        self.base_hp = int(row["hp"].values[0])
        self.base_attack = int(row["attack"].values[0])
        self.base_defense = int(row["defense"].values[0])
        self.base_sp_attack = int(row["sp_atk"].values[0])
        self.base_sp_defense = int(row["sp_def"].values[0])
        self.base_speed = int(row["speed"].values[0])
        self.hp = self.base_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.sp_attack = self.base_sp_attack
        self.sp_defense = self.base_sp_defense
        self.speed = self.base_speed
        self.set_initial_stats()

    def set_initial_stats(self):
        for _ in range(1, self.initial_level):
            self.hp = round(self.hp + (110 + self.base_hp) / 100)
            self.attack = round(self.attack + (5 + self.base_attack) / 100)
            self.defense = round(self.defense + (5 + self.base_defense) / 100)
            self.sp_attack = round(self.sp_attack + (5 + self.base_sp_attack) / 100)
            self.sp_defense = round(self.sp_defense + (5 + self.base_sp_defense) / 100)
            self.speed = round(self.speed + (5 + self.base_speed) / 100)
        print(f"Estadísticas después de subir de nivel: {self}")

    def combat_stats(self, accuracy="100%", evasion="100%"):
        self.accuracy = accuracy
        self.evasion = evasion

    def __str__(self):
        return (
            f"HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.sp_attack}, Sp. Defense: {self.sp_defense}, Speed: {self.speed}"
        )


class Move:
    # Represents a single Pokemon move
    def __init__(self, move_id, name, type_, power, accuracy, pp, category):
        self.id = move_id
        self.name = name
        self.type = type_
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.type}) | Power: {self.power}, Accuracy: {self.accuracy}, PP: {self.pp}, Category: {self.category}"


class Moveset:
    # Manages the moveset of a Pokemon based on its Pokedex number and level
    def __init__(self, pokedex_num: int, level: int):
        self.current_dir = Path(__file__).parent  # Actual directory of pokemon.py
        self.moves_path = self.current_dir / "utils" / "moves.csv"  # Path to moves.csv
        self.pokemon_moves_path = (
            self.current_dir / "utils" / "pokemon_moves.csv"
        )  # Path to pokemon_moves.csv

        self.pokedex_num = pokedex_num
        self.level = level

        # Load both CSVs once for efficiency
        self._moves_df = pd.read_csv(self.moves_path)  # Load moves data once
        self._pokemon_moves_df = pd.read_csv(
            self.pokemon_moves_path
        )  # Load pokemon_moves data once

        # Now load and select moves using cached dataframes
        self.available_moves = self._load_available_moves()
        self.current_moves = self._select_current_moves()

    def _load_available_moves(self):
        # Uses the CSV files to load all moves the Pokemon can learn up to its current level
        pm_df = self._pokemon_moves_df.copy()  # Work on a copy to avoid side effects
        # Filter by this Pokemon's Pokedex number
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        # Filter by level learned
        pm_df = pm_df[pm_df["level_learned"] <= self.level]

        # Merge to get full move details
        merged = pm_df.merge(self._moves_df, left_on="move_id", right_on="id")

        # Collect Move objects (optimized with itertuples)
        moves = [
            Move(
                move_id=row.id,
                name=row.name,
                type_=row.type,
                power=row.power,
                accuracy=row.accuracy,
                pp=row.pp,
                category=row.category,
            )
            for row in merged.itertuples(index=False)
        ]
        return moves

    def _select_current_moves(self):
        # Selects up to 4 moves based on the highest level learned
        if not self.available_moves:
            return []

        # Load pokemon_moves to filter by level learned
        pm_df = self._pokemon_moves_df.copy()
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        pm_df = pm_df[pm_df["level_learned"] <= self.level]
        pm_df = pm_df.sort_values(by="level_learned", ascending=False)
        pm_df = pm_df.drop_duplicates(subset=["move_id"], keep="first")
        top_moves_ids = pm_df["move_id"].head(4).tolist()
        # Select corresponding Move objects
        selected = []
        ids = []

        for m in self.available_moves:
            # Check if the move's ID is in the top moves list
            if m.id in top_moves_ids and m.id not in ids:
                selected.append(m)
                ids.append(m.id)

        return selected

    def show_moves(self):
        # Displays the current moves of the Pokemon
        if not self.current_moves:
            print("This Pokemon has no moves.")
            return
        for move in self.current_moves:
            print(f"- {move}")

    def get_moves_names(self):
        # Returns a list of the names of the current moves
        return [m.name for m in self.current_moves]

    def __str__(self):
        """Return a string representation of the current moveset."""
        if not self.current_moves:
            return "Moveset: (no moves)"
        return "Moveset: " + ", ".join(move.name for move in self.current_moves)


if __name__ == "__main__":
    bulbasaur = Pokemon("bulbasaur", 1, "grass", "blue", "male", 3)
    print(bulbasaur)
    bulbasaur.attack()
    print(bulbasaur.get_stats())
    charmander = Pokemon("charmander", 4, "fire", "orange", "male")
    print(charmander)
    charmander.attack()
    print(charmander.get_stats())
