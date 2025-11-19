### TODO: Implement the battle field logic
# Turns management
# Uses engine to compute damage and update stats
# Defines win/loss conditions

from pokemon import Pokemon, Move
from engine import CombatEngine
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

    def __init__(self, name):
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
            df = df[~df["name"].isin(pokemon_used)]

        for _, row in df.iterrows():
            print(f"{int(row['pokedex_number']):>3} | {row['name']} | {row['evolution_level']}")
        return df

    def choose_pokemon(self):
        """Interactively choose up to 6 Pokémon for this trainer.
        """
        while True:
            print(f"{self.name}, choose Pokémon #{len(self.pokemon) + 1} for the battle.")

            already_chosen = [p.name for p in self.pokemon]
            df = self.pokemon_available(already_chosen)

            chosen = int(input("Enter pokédex number: ").strip())

            row = df.loc[df["pokedex_number"] == chosen]
            if row.empty:
                print("Invalid number. Try again.")
                continue
            row = row.iloc[0]
            name = row["name"]
            pokedex_number = int(row["pokedex_number"])
            poke_type = input(f"Enter the primary type for {name}: ").strip().capitalize()
            self.pokemon.append(Pokemon(name, pokedex_number, poke_type, "gray", "male"))
            print(f"\n✅ {self.name} chose {name} for the battle!")

            if len(self.pokemon) == 6:
                break

        return self.pokemon


class Field:
    """Manage a battle between two `Trainer` instances.
    
    - Track each trainer's team and active Pokémon
    - Keep combat HP for each Pokémon
    - Handle turns, switches, attacks
    """

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.__team1 = trainer1.pokemon.copy()  # Copy to avoid modifying original
        self.__team2 = trainer2.pokemon.copy()
        self.__active1 = self.__team1[0] if self.__team1 else None
        self.__active2 = self.__team2[0] if self.__team2 else None
        self.__combat_hp = {}
        self.__number_turn = 0

        for pokemon in self.__team1:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp
            pokemon.get_stats().combat_stats()
            
        for pokemon in self.__team2:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp
            pokemon.get_stats().combat_stats()
            
            
    def get_team1(self):
        return self.__team1

    def get_team2(self):
        return self.__team2

    def get_active1(self):
        return self.__active1

    def get_active2(self):
        return self.__active2
    
    def get_turn_number(self):
        return self.__number_turn

    def get_combat_hp(self, pokemon):
        return self.__combat_hp.get(pokemon, 0)

    def set_combat_hp(self, pokemon, value):
        self.__combat_hp[pokemon] = max(0, value)

    def reduce_hp(self, pokemon, damage):
        current = self.get_combat_hp(pokemon)
        self.set_combat_hp(pokemon, current - damage)

    def end_battle(self):
        """Check if the battle has ended"""
        team1_alive = any(self.get_combat_hp(p) > 0 for p in self.__team1)
        team2_alive = any(self.get_combat_hp(p) > 0 for p in self.__team2)
        if team1_alive and team2_alive:
            return False
        else:
            return True  
    
    def winner_game(self):
        """Return the winning trainer"""
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
        """Check if trainer needs to switch pokemon after one of them is defeat"""
        active = self.__active1 if trainer == self.trainer1 else self.__active2
        if active is None:
            return False
        return self.get_combat_hp(active) <= 0 and len(self.pokemon_available(trainer)) > 0

    
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

    
    
    def execute_attack(self, attacker: Pokemon, defender: Pokemon, move: Move):
        """Execute an attack and return damage"""
        engine = CombatEngine(
            attacker=attacker,
            defender=defender,
            move=move,
            attacker_moves=[],
            defender_moves=[]
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
            messages.append(f"{self.trainer1.name} sent out {self.__active1._name}!")
            
            self.__active2 = action2["new_pokemon"]
            messages.append(f"{self.trainer2.name} sent out {self.__active2._name}!")
            return (True, messages)

        elif action1["action"] == "switch":
            self.__active1 = action1["new_pokemon"]
            messages.append(f"{self.trainer1.name} sent out {self.__active1._name}!")
            
            if action2["action"] == "attack":
                messages.append(f"{self.__active2._name} used {action2['move'].name}!")
                damage, crit, msg = self.execute_attack(self.__active2, self.__active1, action2["move"])
                messages.append(msg)
            return (True, messages)

        elif action2["action"] == "switch":
            self.__active2 = action2["new_pokemon"]
            messages.append(f"{self.trainer2.name} sent out {self.__active2._name}!")
            
            if action1["action"] == "attack":
                messages.append(f"{self.__active1._name} used {action1['move'].name}!")
                damage, crit, msg = self.execute_attack(self.__active1, self.__active2, action1["move"])
                messages.append(msg)
            return (True, messages)

        if action1["action"] == "attack" and action2["action"] == "attack":
            if self.__active1.get_stats().speed >= self.__active2.get_stats().speed:
                messages.append(f"{self.__active1._name} is faster!")
                messages.append(f"{self.__active1._name} used {action1['move'].name}!")
                damage, crit, msg = self.execute_attack(self.__active1, self.__active2, action1["move"])
                messages.append(msg)

                if self.get_combat_hp(self.__active2) > 0:
                    messages.append(f"{self.__active2._name} used {action2['move'].name}!")
                    damage, crit, msg = self.execute_attack(self.__active2, self.__active1, action2["move"])
                    messages.append(msg)
            else:
                messages.append(f"{self.__active2._name} is faster!")
                messages.append(f"{self.__active2._name} used {action2['move'].name}!")
                damage, crit, msg = self.execute_attack(self.__active2, self.__active1, action2["move"])
                messages.append(msg)

                if self.get_combat_hp(self.__active1) > 0:
                    messages.append(f"{self.__active1._name} used {action1['move'].name}!")
                    damage, crit, msg = self.execute_attack(self.__active1, self.__active2, action1["move"])
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
        """Return a simple text health bar representation."""
        filled = int((current_hp / max_hp) * bar_length)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {current_hp}/{max_hp} HP"
