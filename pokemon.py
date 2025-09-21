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
    

    def attack(self):
        print(f"{self.name} is attacking!") 

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to level {self.level}!")

    def __str__(self):
        return f"{self.name} (#{self.pokedex_num}) - Type: {self.main_type}, Level: {self.level}"

class PokemonType(Pokemon):
    weaknesses = []
    resistances = []
    immunities = []
    main_type = None

    def __init__(self, name, pokedex_num, main_type, color, sex, level=1):
        super().__init__(name, pokedex_num, color, sex, level)
        self.main_type = main_type

    def receive_attack(self, attack_type):
        if attack_type in self.immunities:
            print("It's inmune!")
        elif attack_type in self.weaknesses:
            print("It's super effective!")
        elif attack_type in self.resistances:
            print("It's not very effective...")
        else:
            print("It's effective.")


class Ghost(PokemonType):
    weaknesses = ["ghost", "dark"]
    resistances = ["poison", "bug"]
    immunities = ["normal", "fighting"]

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "ghost", color, sex, level)


class Fire(PokemonType):
    weaknesses = ["water", "rock", "ground"]
    resistances = ["grass", "bug", "ice", "steel", "fairy"]
    immunities = []

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "fire", color, sex, level)


class Poison(PokemonType):
    weaknesses = ["psychic", "ground"]
    resistances = ["fighting", "poison", "grass", "bug", "fairy"]
    immunities = []

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "poison", color, sex, level)


class Water(PokemonType):
    weaknesses = ["grass", "electric"]
    resistances = ["fire", "water", "steel", "ice"]
    immunities = []

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "water", color, sex, level)


class Dragon(PokemonType):
    weaknesses = ["dragon", "ice", "fairy"]
    resistances = ["fire", "water", "grass", "electric"]
    immunities = []

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "dragon", color, sex, level)


class Normal(PokemonType):
    weaknesses = ["fighting"]
    resistances = []
    immunities = ["ghost"]

    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "normal", color, sex, level)
        
class Steel(PokemonType):
    weaknesses = ["Fire", "Fighting","Ground"]
    resistances = ["Normal", "Bug", "Flying", "Steel", "Rock", "Grass", "Psychic", "Ice", "Dragon", "Fairy"]
    immunities = ["Poison"]

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Steel", color, sex, level)

class Fighting(PokemonType):
    weaknesses = ["Flying", "Psychic", "Fairy"]
    resistances = ["Bug", "Rock", "Dark"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fighting", color, sex, level)

class Grass(PokemonType):
    weaknesses = ["Fire", "Flying", "Ice", "Bug", "Poison"]
    resistances = ["Water", "Electric", "Ground", "Grass"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Grass", color, sex, level)

class Rock(PokemonType):
    weaknesses = ["Steel", "Ground", "Water", "Fighting", "Grass"]
    resistances = ["Fire", "Normal", "Flying", "Poison"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Rock", color, sex, level)

class Ground(PokemonType):
    weaknesses = ["Water", "Ice", "Grass"]
    resistances = ["Rock", "Poison"]
    immunities = ["Electric"]

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ground", color, sex, level)

class Flying(PokemonType):
    weaknesses = ["Electric", "Ice", "Rock"]
    resistances = ["Bug", "Fighting", "Grass"]
    immunities = ["Ground"]

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Flying", color, sex, level)
        
class Ice(PokemonType):
    weaknesses = ["Fire", "Fighting", "Rock", "Steel"]
    resistances = ["Ice"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Ice", color, sex, level)


class Psychic(PokemonType):
    weaknesses = ["Bug", "Ghost", "Dark"]
    resistances = ["Fighting", "Psychic"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Psychic", color, sex, level)


class Bug(PokemonType):
    weaknesses = ["Fire", "Flying", "Rock"]
    resistances = ["Fighting", "Ground", "Grass"]
    immunities = []

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Bug", color, sex, level)


class Dark(PokemonType):
    weaknesses = ["Fighting", "Bug", "Fairy"]
    resistances = ["Ghost", "Dark"]
    immunities = ["Psychic"]

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Dark", color, sex, level)


class Fairy(PokemonType):
    weaknesses = ["Poison", "Steel"]
    resistances = ["Fighting", "Bug", "Dark"]
    immunities = ["Dragon"]

    def _init_(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fairy", color, sex, level)

if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass",
        "male",
        "green"
    )
    print(bulbasaur)
    bulbasaur.attack()

