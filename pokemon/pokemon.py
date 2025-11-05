import pandas as pd

from pathlib import Path


class Pokemon:
    current_dir = Path(__file__).parent
    ### TODO: Move to another module
    # If moved, uses import from that module
    csv_path = current_dir / "utils" / "First151Pokemons.csv"
    definition = """
    Pocket Monster
    """

    def __init__(
        self,
        pokemon_name: str,
        pokedex_num: int,
        type: str,
        color: str,
        sex: str,
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
        self._main_type = type
        self._color = color
        self._sex = sex
        self._level = level if level >= 1 and level <= 100 else 1
        # Always creating base stats
        self._stats = Stats(
            csv_path=str(Pokemon.csv_path), 
            pokedex_num=pokedex_num
        )
        # Moveset managed by another class
        self._moveset = Moveset(pokedex_num=self._pokedex_num, level=self._level)

        #! Here logic can be added to modify stats based on level

        # * Changed to protected
        self._weaknesses: list = []
        self._resistances: list = []
        self._immunities: list = []

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
            #? Check where these multipliers come from
            self._stats.hp = round(self._stats.hp * 1.020)
            self._stats.attack = round(self._stats.attack * 1.017)
            self._stats.defense = round(self._stats.defense * 1.016)
            self._stats.sp_attack = round(self._stats.sp_attack * 1.017)
            self._stats.sp_defense = round(self._stats.sp_defense * 1.016)
            self._stats.speed = round(self._stats.speed * 1.015)
            
            print(f"{self._name} leveled up to level {self._level}!")
        else:
            print(f"{self._name} is already max level!")

    def attack(self) -> str:
        ### TODO: Return necessary information to compute attack
        return f"{self._name} is attacking!"

    def receive_attack(self, attack_type):
        ### TODO: Return necessary information to compute damage
        if attack_type in self._immunities:
            return "It's inmune!"
        elif attack_type in self._weaknesses:
            return "It's super effective!"
        elif attack_type in self._resistances:
            return "It's not very effective..."
        else:
            return "It's effective."

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
            "main_type": self._main_type,
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
    
    def get_moveset(self):
        return self._moveset
    
    def set_moveset(self, new_moveset: "Moveset"):
        self._moveset = new_moveset

    def show_moves(self):
        self._moveset.show_moves()

    def __str__(self):
        return (f"{self._name} (#{self._pokedex_num}) - "
                f"Type: {self._main_type}, Level: {self._level}")


### TODO: Move to another module      
class Stats():
    def __init__(self, csv_path: str, pokedex_num: int):
        df = pd.read_csv(csv_path)
        row = df.loc[df['pokedex_number'] == pokedex_num]
        self.base_hp = int(row['hp'].values[0])
        self.base_attack = int(row['attack'].values[0])
        self.base_defense = int(row['defense'].values[0])
        self.base_sp_attack = int(row['sp_atk'].values[0])
        self.base_sp_defense = int(row['sp_def'].values[0])
        self.base_speed = int(row['speed'].values[0])
        self.hp = self.base_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.sp_attack = self.base_sp_attack
        self.sp_defense = self.base_sp_defense
        self.speed = self.base_speed
    
    def __str__(self):
        return (
            f"HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.sp_attack}, Sp. Defense: {self.sp_defense}, Speed: {self.speed}"
        )

class Move:
    # Represents a single Pokemon move
    def __init__(self, move_id, name, type_, power, accuracy, pp):
        self.id = move_id
        self.name = name
        self.type = type_
        self.power = power
        self.accuracy = accuracy
        self.pp = pp

    def __str__(self):
        return f"{self.name} ({self.type}) | Power: {self.power}, Accuracy: {self.accuracy}, PP: {self.pp}"


class Moveset:
    # Manages the moveset of a Pokemon based on its Pokedex number and level
    def __init__(self, pokedex_num: int, level: int):
        self.current_dir = Path(__file__).parent # Actual directory of moveset.py
        self.moves_path = self.current_dir / "utils" / "moves.csv" # Path to moves.csv
        self.pokemon_moves_path = self.current_dir / "utils" / "pokemon_moves.csv" # Path to pokemon_moves.csv

        self.pokedex_num = pokedex_num
        self.level = level
        self.available_moves = self._load_available_moves()
        self.current_moves = self._select_current_moves()

    def _load_available_moves(self):
        # Uses the CSV files to load all moves the Pokemon can learn up to its current level
        moves_df = pd.read_csv(self.moves_path) # Load moves data 
        pm_df = pd.read_csv(self.pokemon_moves_path) # Load pokemon_moves data -> moves learnable by each Pokemon

        # Filter by this Pokemon's Pokedex number
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        # Filter by level learned
        pm_df = pm_df[pm_df["level_learned"] <= self.level]

        # Merge to get full move details
        merged = pm_df.merge(moves_df, left_on="move_id", right_on="id")

        moves = [] # collect Move objects
        for i, row in merged.iterrows():
            move = Move(
                move_id=row["id"],
                name=row["name"],
                type_=row["type"],
                power=row["power"],
                accuracy=row["accuracy"],
                pp=row["pp"]
            )
            moves.append(move)
        return moves

    def _select_current_moves(self):
        # Selects up to 4 moves based on the highest level learned
        if not self.available_moves:
            return []
        # Load pokemon_moves to filter by level learned
        pm_df = pd.read_csv(self.pokemon_moves_path)
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        pm_df = pm_df[pm_df["level_learned"] <= self.level]
        pm_df = pm_df.sort_values(by="level_learned", ascending=False)
        top_moves_ids = pm_df["move_id"].head(4).tolist()

        # Select corresponding Move objects
        selected = []  

        for m in self.available_moves:
            # Check if the move's ID is in the top moves list
            if m.id in top_moves_ids:
                selected.append(m)

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

    def combat_stats(self, accuracy = "100%", evasion = "100%"):
        self.accuracy = accuracy
        self.evasion = evasion

    def __str__(self):
        return (
            f"HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.sp_attack}, Sp. Defense: {self.sp_defense}, Speed: {self.speed}"
        )


class Normal(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Normal", color, sex, level)
        self._weaknesses = ["Fighting"]
        self._resistances = []
        self._immunities = ["Ghost"]


class Fire(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fire", color, sex, level)
        self._weaknesses = ["Water", "Ground", "Rock"]
        self._resistances = ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"]
        self._immunities = []


class Water(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Water", color, sex, level)
        self._weaknesses = ["Electric", "Grass"]
        self._resistances = ["Fire", "Water", "Ice", "Steel"]
        self._immunities = []


class Grass(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Grass", color, sex, level)
        self._weaknesses = ["Fire", "Ice", "Poison", "Flying", "Bug"]
        self._resistances = ["Water", "Grass", "Electric", "Ground"]
        self._immunities = []


class Electric(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Electric", color, sex, level)
        self._weaknesses = ["Ground"]
        self._resistances = ["Electric", "Flying", "Steel"]
        self._immunities = []


class Ice(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ice", color, sex, level)
        self._weaknesses = ["Fire", "Fighting", "Rock", "Steel"]
        self._resistances = ["Ice"]
        self._immunities = []


class Fighting(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fighting", color, sex, level)
        self._weaknesses = ["Flying", "Psychic", "Fairy"]
        self._resistances = ["Bug", "Rock", "Dark"]
        self._immunities = []


class Poison(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Poison", color, sex, level)
        self._weaknesses = ["Ground", "Psychic"]
        self._resistances = ["Grass", "Fighting", "Poison", "Bug", "Fairy"]
        self._immunities = []


class Ground(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ground", color, sex, level)
        self._weaknesses = ["Water", "Grass", "Ice"]
        self._resistances = ["Poison", "Rock"]
        self._immunities = ["Electric"]


class Flying(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Flying", color, sex, level)
        self._weaknesses = ["Electric", "Ice", "Rock"]
        self._resistances = ["Grass", "Fighting", "Bug"]
        self._immunities = ["Ground"]


class Psychic(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Psychic", color, sex, level)
        self._weaknesses = ["Bug", "Ghost", "Dark"]
        self._resistances = ["Fighting", "Psychic"]
        self._immunities = []


class Bug(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Bug", color, sex, level)
        self._weaknesses = ["Fire", "Flying", "Rock"]
        self._resistances = ["Grass", "Fighting", "Ground"]
        self._immunities = []


class Rock(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Rock", color, sex, level)
        self._weaknesses = ["Water", "Grass", "Fighting", "Ground", "Steel"]
        self._resistances = ["Normal", "Fire", "Poison", "Flying"]
        self._immunities = []


class Ghost(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ghost", color, sex, level)
        self._weaknesses = ["Ghost", "Dark"]
        self._resistances = ["Poison", "Bug"]
        self._immunities = ["Normal", "Fighting"]


class Dragon(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Dragon", color, sex, level)
        self._weaknesses = ["Ice", "Dragon", "Fairy"]
        self._resistances = ["Fire", "Water", "Grass", "Electric"]
        self._immunities = []


class Dark(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Dark", color, sex, level)
        self._weaknesses = ["Fighting", "Bug", "Fairy"]
        self._resistances = ["Ghost", "Dark"]
        self._immunities = ["Psychic"]


class Steel(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Steel", color, sex, level)
        self._weaknesses = ["Fire", "Fighting", "Ground"]
        self._resistances = [
            "Normal",
            "Grass",
            "Ice",
            "Flying",
            "Psychic",
            "Bug",
            "Rock",
            "Dragon",
            "Steel",
            "Fairy",
        ]
        self._immunities = ["Poison"]


class Fairy(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fairy", color, sex, level)
        self._weaknesses = ["Poison", "Steel"]
        self._resistances = ["Fighting", "Bug", "Dark"]
        self._immunities = ["Dragon"]


if __name__ == "__main__":
    bulbasaur = Pokemon("bulbasaur", 1, "grass", "blue", "male")
    print(bulbasaur)
    bulbasaur.attack()
    print(bulbasaur.get_stats())
    charmander = Pokemon("charmander", 4, "fire", "orange", "male")
    charmander.attack()
    print(charmander.get_stats())
