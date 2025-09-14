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


if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass"
    )
    print(bulbasaur)
    bulbasaur.attack()

