import random
import math
from pokemon.pokemon import Pokemon, Move, Stats


# Computes damage based on types and stats
# Source: https://bulbapedia.bulbagarden.net/wiki/Damage (Generation I - Pokémon Stadium)
class CombatEngine:
    """Combat engine for Generation I damage calculations.

    Initialized with attacker and defender Pokémon, the move used, and lists
    of moves previously used by each side.

    The primary public method is `calculate_damage()` which returns a tuple
    `(damage: int, is_critical: bool)`.
    """

    def __init__(
        self,
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        attacker_moves: list,
        defender_moves: list,
    ):
        # Initialize CombatEngine with attacker, defender, move, and moves used by the attacker
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.attacker_moves = attacker_moves
        self.defender_moves = defender_moves

    def calculate_damage(self):
        """Compute damage using helper methods.

        Returns a tuple `(damage, is_critical)` where `damage` is an integer
        and `is_critical` is a boolean indicating whether the hit was critical.
        """
        # Determines if the move hits
        move_hit = self.Hit_Accuracy()
        if not move_hit:
            return 0, False  # If the move misses, damage is 0

        # Get all necessary attributes for the damage calculation
        level = self.attacker.get_attribute("level")
        crit = self.critical_hit()
        power = self.move.power
        A, D = self.attack_defense(crit)
        attacker_types = [self.attacker.get_attribute("type")]
        defender_interactions: dict = {
            "Weaknesses": self.defender.get_attribute("weaknesses"),
            "Resistances": self.defender.get_attribute("resistances"),
            "Immunities": self.defender.get_attribute("immunities"),
        }
        stab = 1.5 if self.move.type in attacker_types else 1.0
        move_type = self.move.type

        type_effectiveness = 1

        # Type-effectiveness calculation
        if move_type in defender_interactions["Immunities"]:
            type_effectiveness *= 0.0

        if type_effectiveness != 0.0:
            if move_type in defender_interactions["Resistances"]:
                type_effectiveness *= 0.5
            if move_type in defender_interactions["Weaknesses"]:
                type_effectiveness *= 2.0

        # Gets a random factor
        random_factor = random.randint(217, 255) / 255

        # Damage calculation
        if crit:  # If it's a critical hit, level is multiplied by 2
            Damage = int(
                ((((2 * level * 2 / 5) + 2) * power * (A / D)) / 50 + 2)
                * stab
                * type_effectiveness
            )
        else:  # Normal damage calculation
            Damage = int(
                ((((2 * level / 5) + 2) * power * (A / D)) / 50 + 2)
                * stab
                * type_effectiveness
            )

        if Damage == 1:  # If damage equals 1, do not apply the random factor
            random_factor = 1

        Damage = math.floor(Damage * random_factor)
        Damage = max(1, Damage)  # Ensure at least 1 damage is dealt

        Damage = Damage
        return Damage, crit

    def critical_hit(self) -> bool:
        """Determine whether the current move is a critical hit.

        A threshold is calculated from the attacker's speed and previous
        moves (for example, if 'Focus Energy' has been used). Returns True
        if a random roll is below the threshold.
        """
        speed = self.attacker.get_stats().speed  # Attacker's speed stat
        # If Focus Energy was used, increase the chance of a critical hit
        if "Focus Energy" in [i.name for i in self.attacker_moves]:
            if self.move.name in ["Crabhammer", "Karate Chop", "Razor Leaf", "Slash"]:
                # Very high critical chance for high-crit moves
                threshold = 255
            else:
                # Increased critical chance for other moves
                threshold = math.floor(((speed + 236) / 4) * 2)
        else:
            if self.move.name in ["Crabhammer", "Karate Chop", "Razor Leaf", "Slash"]:
                # Higher critical chance for high-crit moves
                threshold = math.floor(((speed + 76) / 4) * 8)
            else:
                # Normal critical chance for other moves
                threshold = math.floor((speed + 76) / 4)
        if threshold > 255:
            threshold = 255
        # Roll a random value to determine critical outcome
        value = random.randint(0, 255)
        return value < threshold

    # Determine attack and defense based on Generation I rules
    def attack_defense(self, critical: bool):
        """Compute effective Attack and Defense values for the current move.

        Adjustments include Reflect/Light Screen, Explosion/Selfdestruct effects,
        and handling for stat values above 255. Returns a tuple `(A, D)`.
        """
        # TODO: Implement move categories ("special" vs "physical") in future upgrade.
        # For a future upgrade:
        # if self.move.category == "special":
        #   A = self.attacker.get_stats().sp_attack
        #   D = self.defender.get_stats().sp_defense
        # elif self.move.category == "physical":
        #   A = self.attacker.get_stats().attack
        #   D = self.defender.get_stats().defense

        # As categories are not implemented yet, use physical stats by default
        A = self.attacker.get_stats().attack
        D = self.defender.get_stats().defense

        # Check whether Reflect or Light Screen are active
        if critical:
            reflect = False
            # light_screen = False
        else:
            reflect = "Reflect" in [i.name for i in self.defender_moves]
            # light_screen = "Light Screen" == [i.name for i in self.defender_moves]

        # For a future update:
        # Compute effective defense
        # if not critical:
        #    if self.move.category == "physical" and reflect:
        #        D *= 2
        #    elif self.move.category == "special" and light_screen:
        #        D *= 2

        # Current implementation: only physical moves
        if reflect:
            D *= 2

        if self.move.name in ["Explosion", "Selfdestruct"]:
            D = max(1, math.floor(D / 2))

        # Special case for stats over 255
        if A > 255 or D > 255:
            A = math.floor(A / 4)
            D = math.floor(D / 4)

        if D == 0:
            D = 1

        return A, D

    def Hit_Accuracy(self):
        """Determine whether the move hits its target. Returns True on hit.

        This computes the final hit chance from move accuracy, attacker
        accuracy, and defender evasion, then compares it against a random roll.
        """
        # Compute hit chance based on accuracy and evasion
        move_accuracy = self.move.accuracy
        accuracy_multiplier = 1
        evasion_multiplier = 1
        self.attacker.get_stats().combat_stats()
        self.defender.get_stats().combat_stats()
        if self.attacker.get_stats().accuracy == "100%":
            accuracy_multiplier = 1
        if self.defender.get_stats().evasion == "100%":
            evasion_multiplier = 1

        # Final hit chance
        Accuracy = move_accuracy * accuracy_multiplier * evasion_multiplier

        # Roll to decide if the move hits
        R = random.uniform(0, 100)
        return R < Accuracy
