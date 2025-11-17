import random
import math
from pokemon import Pokemon
from pokemon import Move

# Computes damage base on types and stats
# Source: https://bulbapedia.bulbagarden.net/wiki/Damage (first generation - pokémon stadium )
class CombatEngine: # Class in charge of calculating damage
    def __init__(self, attacker: Pokemon, defender: Pokemon, move: Move, attacker_moves: list, defender_moves: list):
        # Initialize CombatEngine with attacker, defender, move, and moves used by the attacker
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.attacker_moves = attacker_moves
        self.defender_moves = defender_moves

    def calculate_damage(self):
        # Determines if the move hits
        move_hit = self.Hit_Accuracy()
        if move_hit == False:
            return 0, False  # If the move misses, damage is 0
        
        # Gets all the necessary attributes to calculate damage
        level = self.attacker.get_attribute("level")
        crit = self.critical_hit()
        power = self.move.power
        A, D = self.attack_defense(crit)
        attacker_types = [self.attacker.get_attribute("main_type"), self.attacker.get_attribute("type")]
        defender_interactions: dict = {"Weaknesses": self.defender.get_attribute("weaknesses"), "Resistances": self.defender.get_attribute("resistances"), "Immunities": self.defender.get_attribute("immunities")} 
        stab = 1.5 if self.move.type in attacker_types else 1.0
        move_type = self.move.type
        
        # Type effectiveness calculation
        if move_type in defender_interactions["Immunities"]:
            type_effectiveness = 0
        elif move_type in defender_interactions["Resistances"]:
            type_effectiveness = 0.5
        elif move_type in defender_interactions["Weaknesses"]:
            type_effectiveness = 2.0
        else:
            type_effectiveness = 1.0
        
        # Gets a random factor
        random_factor = random.randint(217, 255) / 255

        # Damage calculation
        if crit == True: # If it's a critical hit, level is multiplied by 2
            Damage = int(((((2*level*2/5)+2)*power*(A/D))/50+2)*stab*type_effectiveness)
        else: # Normal damage calculation
            Damage = int(((((2*level/5)+2)*power*(A/D))/50+2)*stab*type_effectiveness)
        
        if Damage == 1: # If damage is 1, no random factor is applied
            random_factor = 1
        
        if Damage < 1: # Ensures minimum damage of 1
            Damage = 1

        Damage = math.floor(Damage*random_factor)
        Damage = int(Damage)
        return Damage, crit # Returns the final damage value as an integer

    def critical_hit(self) -> bool: # Determines if the move is a critical hit
        velocidad = self.attacker.get_stats().speed # Get the speed stat of the attacker
        if "Focus Energy" in self.attacker_moves:
            # If Focus Energy has been used, increase critical hit chance
            if self.move.name in ["Crabhammer", " Karate Chop", "Razor Leaf", "Slash"]:
                # Almost guaranteed critical hit for high crit moves
                threshold = 255
            else:
                # Increased critical hit chance for other moves
                threshold = math.floor(((velocidad + 236)/4)*2)
        else:
            if self.move.name in ["Crabhammer", " Karate Chop", "Razor Leaf", "Slash"]:
                # High critical hit chance for high crit moves
                threshold = math.floor(((velocidad + 76)/4)*8)
            else:
                # Normal critical hit chance for other moves
                threshold = math.floor((velocidad + 76)/4)
        if threshold > 255:
            threshold = 255
        # Generate a random value to determine if it's a critical hit
        value = random.randint(0,255)
        return value < threshold  # If value is less than threshold, it's a critical hit

    #determines attack and defence on bases of first generation rules
    def attack_defense(self, critical: bool):
        
        # Gets the base attack and defense values using the category of the move
        # if self.move.category == "special":
        #   A = self.attacker.get_stats().sp_attack
        #   D = self.defender.get_stats().sp_defense
        # elif self.move.category == "physical":
        #   A = self.attacker.get_stats().attack 
        #   D = self.defender.get_stats().defense

        # As it is not implemented yet, the physical values are used by default
        A = self.attacker.get_stats().attack 
        D = self.defender.get_stats().defense
       
        # Finds if reflect or light screen are active
        if critical:
            reflect = False
            light_screen = False
        else:
            reflect = "Reflect" in self.defender_moves
            light_screen = "Light Screen" in self.defender_moves

        # Gets effective defense
        if not critical:
            if self.move.type == "physical" and reflect:
                D *= 2
            elif self.move.type == "special" and light_screen:
                D *= 2

        if self.move.name in ["Explosion", "Selfdestruct"]:
            D = max(1, math.floor(D / 2))

        # Special Case for stats over 255
        if A > 255 or D > 255:
            A = math.floor(A / 4)
            D = math.floor(D / 4)

        if D == 0:
            D = 1

        return A, D # Returns the effective attack and defense values
    
    def Hit_Accuracy(self):
        # Determines if the move hits based on accuracy and evasion
        move_accuracy = self.move.accuracy
        if self.attacker.get_stats().accuracy == "100%"
            accuracy_multiplier = 1
        if self.defender.get_stats().evasion == "100%"
            evasion_multiplier = 1

        # Calculate final hit chance
        Accuracy = move_accuracy * accuracy_multiplier * evasion_multiplier

        # Generate a random value to determine if the move hits
        R = random.uniform(0, 255)
        return R < Accuracy  # If value is less than the accuracy, the move hits
