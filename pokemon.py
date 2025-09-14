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
            type: str
        ) -> None:
        """
        Creates a basic pokemon

        Args:
            name (int): Pokemon's name in lowercase
            pokedex_num (int): Number in the national pokedex
            type (str): Main type of the pokemon
        Returns:
            

        Raises:


        """

        self.name = name
        self.pokedex_num = pokedex_num
        self.main_type = type


    def attack(self):
        print(f"{self.name} is attacking!") 

    
if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass"
    )
    bulbasaur.attack()

