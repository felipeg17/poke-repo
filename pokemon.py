import os
import pdb

from pprint import pprint

from typing import List

class Type:
    def __init__(self, name: str, weaknesses=None, resistances=None, immunities=None):
        self.name = name
        self.weaknesses = weaknesses if weaknesses else []
        self.resistances = resistances if resistances else []
        self.immunities = immunities if immunities else []

    def __str__(self):
        return self.name


class Pokemon:
    def __init__(self, name: str, pokedex_num: int, types: List[Type], color: str, sex: str, level: int = 1):
        self.name = name
        self.pokedex_num = pokedex_num
        self.types = types
        self.color = color
        self.sex = sex
        self.level = level

    def attack(self):
        print(f"{self.name} is attacking!")

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to level {self.level}!")

    def show_info(self):
        type_names = ", ".join([t.name for t in self.types])
        print(f"Pokémon: {self.name} (#{self.pokedex_num})")
        print(f"Type: {type_names}")
        print(f"Color: {self.color}, Sex: {self.sex}, Level: {self.level}")

    def get_weaknesses(self):
        return set(w for t in self.types for w in t.weaknesses)

    def get_resistances(self):
        return set(r for t in self.types for r in t.resistances)

    def get_immunities(self):
        return set(i for t in self.types for i in t.immunities)


normal = Type("Normal", weaknesses=["Fighting"], resistances=[], immunities=["Ghost"])

fire = Type("Fire", weaknesses=["Water", "Rock", "Ground"], resistances=["Grass", "Bug", "Ice", "Steel", "Fairy"])

water = Type("Water", weaknesses=["Grass", "Electric"], resistances=["Fire", "Water", "Steel", "Ice"])

grass = Type("Grass", weaknesses=["Fire", "Flying", "Ice", "Bug", "Poison"], resistances=["Water", "Electric", "Ground", "Grass"])

electric = Type("Electric", weaknesses=["Ground"], resistances=["Electric", "Flying", "Steel"])

ice = Type("Ice", weaknesses=["Fire", "Fighting", "Rock", "Steel"], resistances=["Ice"])

fighting = Type("Fighting", weaknesses=["Flying", "Psychic", "Fairy"], resistances=["Bug", "Rock", "Dark"])

poison = Type("Poison", weaknesses=["Psychic", "Ground"], resistances=["Fighting", "Poison", "Grass", "Bug", "Fairy"])

ground = Type("Ground", weaknesses=["Water", "Ice", "Grass"], resistances=["Rock", "Poison"], immunities=["Electric"])

flying = Type("Flying", weaknesses=["Electric", "Ice", "Rock"], resistances=["Bug", "Fighting", "Grass"], immunities=["Ground"])

psychic = Type("Psychic", weaknesses=["Bug", "Ghost", "Dark"], resistances=["Fighting", "Psychic"])

bug = Type("Bug", weaknesses=["Fire", "Flying", "Rock"], resistances=["Fighting", "Ground", "Grass"])

rock = Type("Rock", weaknesses=["Steel", "Ground", "Water", "Fighting", "Grass"], resistances=["Fire", "Normal", "Flying", "Poison"])

ghost = Type("Ghost", weaknesses=["Ghost", "Dark"], resistances=["Poison", "Bug"], immunities=["Normal", "Fighting"])

dragon = Type("Dragon", weaknesses=["Dragon", "Ice", "Fairy"], resistances=["Fire", "Water", "Grass", "Electric"])

dark = Type("Dark", weaknesses=["Fighting", "Bug", "Fairy"], resistances=["Ghost", "Dark"], immunities=["Psychic"])

steel = Type("Steel", weaknesses=["Fire", "Fighting", "Ground"], resistances=["Normal", "Bug", "Flying", "Steel", "Rock", "Grass", "Psychic", "Ice", "Dragon", "Fairy"], immunities=["Poison"])

fairy = Type("Fairy", weaknesses=["Poison", "Steel"], resistances=["Fighting", "Bug", "Dark"], immunities=["Dragon"])

if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        [grass],
        "blue",
        "male"
    )
    bulbasaur.show_info()
    bulbasaur.attack()