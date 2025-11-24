import random
import math
from pokemon.pokemon import Pokemon, Move


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
        # Initialize CombatEngine with attacker, defender, move, moves used by the attacker and defender, and field
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.attacker_moves = attacker_moves
        self.defender_moves = defender_moves

    def calculate_damage(
        self,
        attack_stats,
        defense_stats,
        sp_attack_stats,
        sp_defense_stats,
        speed_stats,
    ):
        """Compute damage using helper methods.

        Returns a tuple `(damage, is_critical)` where `damage` is an integer
        and `is_critical` is a boolean indicating whether the hit was critical.
        """
        base_power = self.move.power
        status_effect, power = self.status_changes(base_power)
        if not status_effect:
            return 0, False, False

        # Determines if the move hits
        move_hit = self.Hit_Accuracy()
        if self.move.power == 0:
            return 0, False, move_hit  # If the move has no power, damage is 0

        # Get all necessary attributes for the damage calculation
        level = self.attacker.get_attribute("level")
        crit = self.critical_hit(speed_stats)
        A, D = self.attack_defense(
            crit, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )
        attacker_types = [self.attacker.get_attribute("main_type")]
        defender_interactions: dict = {
            "Weaknesses": self.defender.get_attribute("weaknesses"),
            "Resistances": self.defender.get_attribute("resistances"),
            "Immunities": self.defender.get_attribute("immunities"),
        }
        stab = 1.5 if self.move.type in attacker_types else 1.0
        move_type = self.move.type
        # Type-effectiveness calculation
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
        return Damage, crit, move_hit

    def critical_hit(self, speed_stats) -> bool:
        """Determine whether the current move is a critical hit.

        A threshold is calculated from the attacker's speed and previous
        moves (for example, if 'Focus Energy' has been used). Returns True
        if a random roll is below the threshold.
        """
        speed = speed_stats.get(self.attacker, 0)  # Attacker's speed stat
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
    def attack_defense(
        self,
        critical: bool,
        attack_stats,
        defense_stats,
        sp_attack_stats,
        sp_defense_stats,
    ):
        """Compute effective Attack and Defense values for the current move.

        Adjustments include Reflect/Light Screen, Explosion/Selfdestruct effects,
        and handling for stat values above 255. Returns a tuple `(A, D)`.
        """

        if self.move.category == "Special":
            A = sp_attack_stats.get(self.attacker, 0)
            D = sp_defense_stats.get(self.defender, 0)
        elif self.move.category == "Physical":
            A = attack_stats.get(self.attacker, 0)
            D = defense_stats.get(self.defender, 0)

        # Check whether Reflect or Light Screen are active
        if critical:
            reflect = False
            light_screen = False
        else:
            reflect = "Reflect" in [i.name for i in self.defender_moves]
            light_screen = "Light Screen" in [i.name for i in self.defender_moves]

        # Compute effective defense
        if not critical:
            if self.move.category == "Physical" and reflect:
                D *= 2
            elif self.move.category == "Special" and light_screen:
                D *= 2

        # Special case for Explosion and Selfdestruct
        if self.move.name in ["Explosion", "Selfdestruct"]:
            D = max(1, math.floor(D / 2))

        # Special case for stats over 255
        if A > 255 or D > 255:
            A = math.floor(A / 4)
            D = math.floor(D / 4)

        # When a pokemon is burned, its attack is halved
        Status = (
            list(self.attacker.status.keys())
            if self.attacker.status is not None
            else None
        )
        if Status == "Burned":
            A = math.floor(A / 2)

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

    def status_changes(self, power) -> bool:
        """Gets the status of the attacker
        returns true if pokemon can attack, and the power with the modifications if some are implemented
        """
        Status1 = list(self.attacker.status.keys())[0] if self.attacker.status else None
        if not self.attacker.status:
            return True, power

        else:
            for Status in list(self.attacker.status.keys()):
                self.attacker.status[Status] -= 1
                if self.attacker.status[Status] <= 0:
                    del self.attacker.status[Status]
                    print(f"{self.attacker._name} is no longer {Status}")

            if Status == "Paralyzed":
                value = random.randint(0, 100)
                if value <= 25:  # 25% of not attacking
                    print(
                        f"{self.attacker._name} is totally {Status.lower()} and can not attack"
                    )
                    return False, power
                return True, power

            if Status1 == "Burned":
                return True, power

            if Status1 == "Poisoned":
                return True, power

            if Status1 == "Asleep" or Status == "Frozen":
                print(f"{self.attacker._name} is {Status.lower()} and can not attack")
                return False, power

            if Status1 == "Confused":
                value = random.randint(0, 100)
                if value <= 50:  # 50% of attacking himself
                    self.defender = self.attacker
                    self.defender_moves = self.attacker_moves
                    power = 40
                    print(
                        f"{self.attacker._name} is confused and it is attacking itself!"
                    )
                return True, power

            if Status1 == "Seeded":
                return True, power

            if Status1 == "Flinched":
                print(f"{self.attacker._name} is Flinched can not attack!")
                return False, power
        return True, power
