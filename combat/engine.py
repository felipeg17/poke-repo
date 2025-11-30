import random
import math
from pokemon.pokemon import Pokemon, Move


# Computes damage based on types and stats
# Source: https://bulbapedia.bulbagarden.net/wiki/Damage (Generation I - Pokémon Stadium)
class CombatEngine:
    """Combat engine for Generation I damage calculations.

    Initialized with attacker and defender Pokémon, the move used, and lists
    of moves previously used by each side.

    The primary public method is calculate_damage() which returns a tuple
    (damage: int, is_critical: bool, move_hit: bool).

    Attributes:
        attacker (Pokemon): The attacking Pokémon.
        defender (Pokemon): The defending Pokémon.
        move (Move): The move being used.
        attacker_moves (list[Move]): Moves used by the attacker.
        defender_moves (list[Move]): Moves used by the defender.
    """

    def __init__(
        self,
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        attacker_moves: list[Move],
        defender_moves: list[Move],
    ) -> None:
        """Initializes the combat engine.

        Args:
            attacker (Pokemon): The attacking Pokémon.
            defender (Pokemon): The defending Pokémon.
            move (Move): The move to execute.
            attacker_moves (list[Move]): List of moves used by the attacker.
            defender_moves (list[Move]): List of moves used by the defender.
        """
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.attacker_moves: list[Move] = attacker_moves
        self.defender_moves: list[Move] = defender_moves

    def calculate_damage(
        self,
        attack_stats: dict,
        defense_stats: dict,
        sp_attack_stats: dict,
        sp_defense_stats: dict,
        speed_stats: dict,
    ) -> tuple[int, bool, bool]:
        """Computes damage using helper methods.

        Args:
            attack_stats (dict): Dictionary of attack statistics.
            defense_stats (dict): Dictionary of defense statistics.
            sp_attack_stats (dict): Dictionary of special attack statistics.
            sp_defense_stats (dict): Dictionary of special defense statistics.
            speed_stats (dict): Dictionary of speed statistics.

        Returns:
            tuple[int, bool, bool]: A tuple containing:
                - damage (int): The calculated damage value.
                - is_critical (bool): Whether the hit was critical.
                - move_hit (bool): Whether the move hit successfully.
        """
        base_power: int = self.move.power
        status_effect, power = self.status_changes(base_power)

        if not status_effect:
            return 0, False, False

        # Determines if the move hits
        move_hit: bool = self.hit_accuracy()
        if self.move.power == 0:
            return 0, False, move_hit  # If the move has no power, damage is 0

        # Get all necessary attributes for the damage calculation
        level: int = self.attacker.get_attribute("level")
        crit: bool = self.critical_hit(speed_stats)
        A, D = self.attack_defense(
            crit, attack_stats, defense_stats, sp_attack_stats, sp_defense_stats
        )
        attacker_types: list[str] = [self.attacker.get_attribute("type")]
        defender_interactions: dict = {
            "Weaknesses": self.defender.get_attribute("weaknesses"),
            "Resistances": self.defender.get_attribute("resistances"),
            "Immunities": self.defender.get_attribute("immunities"),
        }
        stab: float = 1.5 if self.move.type in attacker_types else 1.0
        move_type: str = self.move.type

        type_effectiveness: float
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
        random_factor: float = random.randint(217, 255) / 255

        # Damage calculation
        if crit:  # If it's a critical hit, level is multiplied by 2
            damage: int = int(
                ((((2 * level * 2 / 5) + 2) * power * (A / D)) / 50 + 2)
                * stab
                * type_effectiveness
            )
        else:  # Normal damage calculation
            damage = int(
                ((((2 * level / 5) + 2) * power * (A / D)) / 50 + 2)
                * stab
                * type_effectiveness
            )

        if damage == 1:  # If damage equals 1, do not apply the random factor
            random_factor = 1

        damage = math.floor(damage * random_factor)
        damage = max(1, damage)  # Ensure at least 1 damage is dealt

        return damage, crit, move_hit

    def critical_hit(self, speed_stats: dict) -> bool:
        """Determines whether the current move is a critical hit.

        A threshold is calculated from the attacker's speed and previous
        moves (for example, if Focus Energy has been used). Returns True
        if a random roll is below the threshold.

        Args:
            speed_stats (dict): Dictionary with speed statistics.

        Returns:
            bool: True if the attack is critical, False otherwise.
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
        value: int = random.randint(0, 255)
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
        """Computes effective Attack and Defense values for the current move.

        Adjustments include Reflect/Light Screen, Explosion/Selfdestruct effects,
        and handling for stat values above 255.

        Args:
            critical (bool): Whether the attack is a critical hit.
            attack_stats (dict): Dictionary of attack statistics.
            defense_stats (dict): Dictionary of defense statistics.
            sp_attack_stats (dict): Dictionary of special attack statistics.
            sp_defense_stats (dict): Dictionary of special defense statistics.

        Returns:
            tuple: A tuple (A, D) with effective Attack and Defense values.
        """

        if self.move.category == "special":
            A = sp_attack_stats.get(self.attacker, 0)
            D = sp_defense_stats.get(self.defender, 0)
        elif self.move.category == "physical":
            A = attack_stats.get(self.attacker, 0)
            D = defense_stats.get(self.defender, 0)

        if A > 255 or D > 255:
            A = math.floor(A / 4)
            D = math.floor(D / 4)

        # Check whether Reflect or Light Screen are active
        if critical:
            reflect = False
            light_screen = False
        else:
            reflect = "Reflect" in [i.name for i in self.defender_moves]
            light_screen = "Light Screen" in [i.name for i in self.defender_moves]

        # Compute effective defense
        if not critical:
            if self.move.category == "physical" and reflect:
                D *= 2
            elif self.move.category == "special" and light_screen:
                D *= 2

        # Special case for Explosion and Selfdestruct
        if self.move.name in ["Explosion", "Selfdestruct"]:
            D = max(1, math.floor(D / 2))

        # When a pokemon is burned, its attack is halved
        Status2 = (
            list(self.attacker.status.keys())
            if self.attacker.status is not None
            else None
        )
        if Status2 == "burned":
            A = math.floor(A / 2)

        if D == 0:
            D = 1

        return A, D

    def hit_accuracy(self) -> bool:
        """Determines whether the move hits its target.

        This computes the final hit chance from move accuracy, attacker
        accuracy, and defender evasion, then compares it against a random roll.

        Returns:
            bool: True if the move hits, False otherwise.
        """
        # Compute hit chance based on accuracy and evasion
        move_accuracy: float = self.move.accuracy
        accuracy_multiplier: float = 1
        evasion_multiplier: float = 1
        self.attacker.get_stats().combat_stats()
        self.defender.get_stats().combat_stats()
        if self.attacker.get_stats().accuracy == "100%":
            accuracy_multiplier = 1
        if self.defender.get_stats().evasion == "100%":
            evasion_multiplier = 1

        # Final hit chance
        Accuracy: float = move_accuracy * accuracy_multiplier * evasion_multiplier

        # Roll to decide if the move hits
        R: float = random.uniform(0, 100)
        return R < Accuracy

    def status_changes(self, power: int) -> tuple[bool, int]:
        """Gets the status of the attacker.

        Args:
            power (int): The base power of the move.

        Returns:
            tuple[bool, int]: A tuple containing:
                - can_attack (bool): True if Pokémon can attack.
                - modified_power (int): The power with modifications if any are applied.
        """
        if not self.attacker.status:
            return True, power

        else:
            for Status in list(self.attacker.status.keys()):
                self.attacker.status[Status] -= 1
                if self.attacker.status[Status] <= 0:
                    del self.attacker.status[Status]
                    print(f"{self.attacker._name} is no longer {Status}")
                    return True, power

            if Status == "paralyzed":
                value = random.randint(0, 100)
                if value <= 25:  # 25% of not attacking
                    print(
                        f"{self.attacker._name} is totally {Status} and can not attack"
                    )
                    return False, power
                return True, power

            if Status == "burned":
                return True, power

            if Status == "poisoned":
                return True, power

            if Status == "asleep" or Status == "frozen":
                print(f"{self.attacker._name} is {Status} and can not attack")
                return False, power

            if Status == "seeded":
                return True, power

            if Status == "flinched":
                print(f"{self.attacker._name} is flinched can not attack!")
                return False, power
        return True, power
