import os
import pdb

from pprint import pprint

class Pokemon:
    definition ="""
    Pocket Monster
    """
    def __init__(
            self,
            name: str,
            pokedex_num: int,
            type: str, 
            color: str,
            sex: str,
            level: int = 1
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
        self.name = name
        self.pokedex_num = pokedex_num
        self.main_type = type
        self.color = color
        self.sex = sex
        self.level = level
        self.weaknesses = []
        self.resistances = []
        self.immunities = []

    def attack(self):
        print(f"{self.name} is attacking!") 

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to level {self.level}!")

    def __str__(self):
        return f"{self.name} (#{self.pokedex_num}) - Type: {self.main_type}, Level: {self.level}"
        
    def receive_attack(self, attack_type):
        if attack_type in self.immunities:
            print("It's inmune!")
        elif attack_type in self.weaknesses:
            print("It's super effective!")
        elif attack_type in self.resistances:
            print("It's not very effective...")
        else:
            print("It's effective.")
            
class Normal(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Normal", color, sex, level)
        self.weaknesses = ["Fighting"]
        self.resistances = []
        self.immunities = ["Ghost"]


class Fire(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fire", color, sex, level)
        self.weaknesses = ["Water", "Ground", "Rock"]
        self.resistances = ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"]
        self.immunities = []


class Water(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Water", color, sex, level)
        self.weaknesses = ["Electric", "Grass"]
        self.resistances = ["Fire", "Water", "Ice", "Steel"]
        self.immunities = []


class Grass(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Grass", color, sex, level)
        self.weaknesses = ["Fire", "Ice", "Poison", "Flying", "Bug"]
        self.resistances = ["Water", "Grass", "Electric", "Ground"]
        self.immunities = []


class Electric(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Electric", color, sex, level)
        self.weaknesses = ["Ground"]
        self.resistances = ["Electric", "Flying", "Steel"]
        self.immunities = []


class Ice(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ice", color, sex, level)
        self.weaknesses = ["Fire", "Fighting", "Rock", "Steel"]
        self.resistances = ["Ice"]
        self.immunities = []


class Fighting(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fighting", color, sex, level)
        self.weaknesses = ["Flying", "Psychic", "Fairy"]
        self.resistances = ["Bug", "Rock", "Dark"]
        self.immunities = []


class Poison(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Poison", color, sex, level)
        self.weaknesses = ["Ground", "Psychic"]
        self.resistances = ["Grass", "Fighting", "Poison", "Bug", "Fairy"]
        self.immunities = []


class Ground(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ground", color, sex, level)
        self.weaknesses = ["Water", "Grass", "Ice"]
        self.resistances = ["Poison", "Rock"]
        self.immunities = ["Electric"]


class Flying(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Flying", color, sex, level)
        self.weaknesses = ["Electric", "Ice", "Rock"]
        self.resistances = ["Grass", "Fighting", "Bug"]
        self.immunities = ["Ground"]


class Psychic(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Psychic", color, sex, level)
        self.weaknesses = ["Bug", "Ghost", "Dark"]
        self.resistances = ["Fighting", "Psychic"]
        self.immunities = []


class Bug(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Bug", color, sex, level)
        self.weaknesses = ["Fire", "Flying", "Rock"]
        self.resistances = ["Grass", "Fighting", "Ground"]
        self.immunities = []


class Rock(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Rock", color, sex, level)
        self.weaknesses = ["Water", "Grass", "Fighting", "Ground", "Steel"]
        self.resistances = ["Normal", "Fire", "Poison", "Flying"]
        self.immunities = []


class Ghost(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ghost", color, sex, level)
        self.weaknesses = ["Ghost", "Dark"]
        self.resistances = ["Poison", "Bug"]
        self.immunities = ["Normal", "Fighting"]


class Dragon(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Dragon", color, sex, level)
        self.weaknesses = ["Ice", "Dragon", "Fairy"]
        self.resistances = ["Fire", "Water", "Grass", "Electric"]
        self.immunities = []


class Dark(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Dark", color, sex, level)
        self.weaknesses = ["Fighting", "Bug", "Fairy"]
        self.resistances = ["Ghost", "Dark"]
        self.immunities = ["Psychic"]


class Steel(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Steel", color, sex, level)
        self.weaknesses = ["Fire", "Fighting", "Ground"]
        self.resistances = [
            "Normal", "Grass", "Ice", "Flying", "Psychic", "Bug",
            "Rock", "Dragon", "Steel", "Fairy"
        ]
        self.immunities = ["Poison"]


class Fairy(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fairy", color, sex, level)
        self.weaknesses = ["Poison", "Steel"]
        self.resistances = ["Fighting", "Bug", "Dark"]
        self.immunities = ["Dragon"]

if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass",
        "blue",
        "male"
    )
    print(bulbasaur)
    bulbasaur.attack()
