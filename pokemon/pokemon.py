import os
import pdb
import pandas as pd

from pprint import pprint

class Pokemon:
    csv_path = "utils/First30Pokemons.csv"
    Pocket Monster
    """
    def __init__(
            self,
            pokemon_name: str,
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
        self.__name = pokemon_name
        self.__pokedex_num = pokedex_num
        self.__main_type = type
        self.__color = color
        self.__sex = sex
        self.__level = level
        self.__stats = Stats(Pokemon.csv_path, pokedex_num)
        #* Changed to protected
        self._weaknesses = []
        self._resistances = []
        self._immunities = []

    def attack(self) -> str:
        return f"{self.__name} is attacking!"

    def level_up(self, hp, attack, defense, spattack, spdefense, speed):
        if self.__level < 100:
            self.__level += 1
            self.__stats.hp = round(self.__stats.hp * 1.020)
            self.__stats.attack = round(self.__stats.attack * 1.017)
            self.__stats.defense = round(self.__stats.defense * 1.016)
            self.__stats.sp_attack = round(self.__stats.sp_attack * 1.017)
            self.__stats.sp_defense = round(self.__stats.sp_defense * 1.016)
            self.__stats.speed = round(self.__stats.speed * 1.015)
            
            print(f"{self.__name} leveled up to level {self.__level}!")
        else:
            print(f"{self.__name} is already max level!")

    def __str__(self):
        return f"{self.__name} (#{self.__pokedex_num}) - Type: {self.__main_type}, Level: {self.__level}"
        
    def receive_attack(self, attack_type):
        if attack_type in self._immunities:
            return "It's inmune!"
        elif attack_type in self._weaknesses:
            return "It's super effective!"
        elif attack_type in self._resistances:
            return "It's not very effective..."
        else:
            return "It's effective."
            
    def stats(self):
        return self.__stats
        
class Stats():
    def __init__(self, csv_path, pokedex_num):
        df = pd.read_csv(csv_path)
        row = df.loc[df['Pokedex Number'] == pokedex_num]
        self.base_hp = int(row['HP'].values[0])
        self.base_attack = int(row['Attack'].values[0])
        self.base_defense = int(row['Defense'].values[0])
        self.base_sp_attack = int(row['Sp. Attack'].values[0])
        self.base_sp_defense = int(row['Sp. Defense'].values[0])
        self.base_speed = int(row['Speed'].values[0])
        self.hp = self.base_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.sp_attack = self.base_sp_attack
        self.sp_defense = self.base_sp_defense
        self.speed = self.base_speed
    def combatstats(self, accuracy = "100%", evasion = "100%"):
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
            "Normal", "Grass", "Ice", "Flying", "Psychic", "Bug",
            "Rock", "Dragon", "Steel", "Fairy"
        ]
        self._immunities = ["Poison"]

class Fairy(Pokemon):
    def __init__(self, name, pokedex_num, color, sex, level=1):
        super().__init__(name, pokedex_num, "Fairy", color, sex, level)
        self._weaknesses = ["Poison", "Steel"]
        self._resistances = ["Fighting", "Bug", "Dark"]
        self._immunities = ["Dragon"]

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
    print(bulbasaur.stats())
    charmander = Pokemon(
        "charmander",
        4,
        "fire",
        "orange",
        "male"
    )
    charmander.attack()
    print(charmander.stats())
