### TODO: Implement the battle field logic
# Include:
# Pokemon definition
# Turns management
# Uses engine to compute damage and update stats
# Defines win/loss conditions

from pokemon import Pokemon
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

        Prompts the user to enter a pokédex number and the Pokémon's type.
        Returns the list of chosen `Pokemon` objects.
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

    Responsibilities:
    - Track each trainer's team and active Pokémon
    - Keep combat HP for each Pokémon
    - Handle turns, switches, attacks, and victory/defeat
    """

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.__team1 = trainer1.pokemon
        self.__team2 = trainer2.pokemon
        self.__active1 = trainer1.pokemon[0] if trainer1.pokemon else None
        self.__active2 = trainer2.pokemon[0] if trainer2.pokemon else None
        self.__combat_hp = {}
        self.__number_turn = 0

        for pokemon in self.__team1:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp

        for pokemon in self.__team2:
            self.__combat_hp[pokemon] = pokemon.get_stats().hp

    def get_team1(self):
        return self.__team1

    def get_team2(self):
        return self.__team2

    def get_active1(self):
        return self.__active1

    def get_active2(self):
        return self.__active2

    def set_active1(self):
        """Prompt trainer1 to choose the active Pokémon from their team."""
        print(f"\n{self.trainer1.name}, select your active Pokémon:")
        for i, pokemon in enumerate(self.__team1):
            print(f"{i + 1}. {pokemon._name} (Pokedex #{pokemon.pokedex_number})")

        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(self.__team1):
                    self.__active1 = self.__team1[choice]
                    print(f"Go, {self.__active1._name}!")
                    return self.__active1
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Enter a valid number.")

    def set_active2(self):
        """Prompt trainer2 to choose the active Pokémon from their team."""
        print(f"{self.trainer2.name}, select your active Pokémon:")
        for i, pokemon in enumerate(self.__team2):
            print(f"{i + 1}. {pokemon._name} (Pokedex #{pokemon.pokedex_number})")

        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(self.__team2):
                    self.__active2 = self.__team2[choice]
                    print(f"Go, {self.__active2._name}!")
                    return self.__active2
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Enter a valid number.")

    def health_bar(self, current_hp, max_hp, bar_length=20):
        """Return a simple text health bar representation."""
        filled = int((current_hp / max_hp) * bar_length)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty

        return f"[{bar}] {current_hp}/{max_hp} HP"

    def player_turn(self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon):
        """Handle a single player's turn and return an action dict.

        Action dict examples:
        - {"action": "attack", "move": Move}
        - {"action": "switch", "new_pokemon": Pokemon}
        - {"action": "surrender"}
        """
        active_hp = self.get_combat_hp(active_pokemon)
        enemy_hp = self.get_combat_hp(enemy_pokemon)

        print(f"""
        {50 * "="}
        Turn: {trainer.name}
        {active_pokemon._name:<20} VS {enemy_pokemon._name:>20}
        {self.health_bar(active_hp, active_pokemon._stats.hp)}  {self.health_bar(enemy_hp, enemy_pokemon._stats.hp)}
        {50 * "="}
        """)

        choice = int(input("""
              (1) Attack
              (2) Switch Pokémon
              (0) Surrender
              """))
        if choice == 1:
            moves = active_pokemon.get_moveset().current_moves

            print(f"\n{30 * '='}")
            print(" Attacks:")
            for i, move in enumerate(moves, 1):
                print(f"({i}) {move}")
            print(f"{30 * '='}")

            try:
                choice_move = int(input("Choose: "))
                if choice_move == 0:
                    return self.player_turn(trainer, active_pokemon, enemy_pokemon)
                elif 1 <= choice_move <= len(moves):
                    chosen_move = moves[choice_move - 1]
                    print(f"{active_pokemon._name} used {chosen_move.name}!")
                    return {"action": "attack", "move": chosen_move}
            except ValueError:
                print("Enter a valid number.")
                return self.player_turn(trainer, active_pokemon, enemy_pokemon)

        elif choice == 2:
            team = trainer.pokemon
            print(f"{30 * '='}")
            print("Your team:")

            for i, pokemon in enumerate(team, 1):
                current_hp = self.get_combat_hp(pokemon)
                max_hp = pokemon._stats.hp
                hp_bar = self.health_bar(current_hp, max_hp, bar_length=15)

                if pokemon == active_pokemon:
                    status = " - (Active)"
                elif current_hp <= 0:
                    status = " (Fainted)"
                else:
                    status = ""

                print(f"({i}) {pokemon._name} {hp_bar}{status}")
            print(f"{30 * '='}")

            try:
                choice_pkm = int(input("\nChoose a Pokémon (0 to go back): "))

                if choice_pkm == 0:
                    return self.player_turn(trainer, active_pokemon, enemy_pokemon)
                elif 1 <= choice_pkm <= len(team):
                    new_pokemon = team[choice_pkm - 1]

                    if new_pokemon == active_pokemon:
                        print("That Pokémon is already in battle!")
                        return self.player_turn(trainer, active_pokemon, enemy_pokemon)
                    elif self.get_combat_hp(new_pokemon) <= 0:
                        print("That Pokémon has fainted!")
                        return self.player_turn(trainer, active_pokemon, enemy_pokemon)
                    else:
                        print(f"Go, {new_pokemon._name}!")
                        return {"action": "switch", "new_pokemon": new_pokemon}
                else:
                    print("Invalid option.")
                    return self.player_turn(trainer, active_pokemon, enemy_pokemon)
            except ValueError:
                print(" Enter a valid number.")

            return self.player_turn(trainer, active_pokemon, enemy_pokemon)

        elif choice == 0:
            confirm = input(f"Are you sure you want to surrender, {trainer.name}? (y/n) ")
            if confirm.lower() == 'y':
                return {"action": "surrender"}
            else:
                return self.player_turn(trainer, active_pokemon, enemy_pokemon)

    def get_combat_hp(self, pokemon):
        return self.__combat_hp.get(pokemon, 0)

    def set_combat_hp(self, pokemon, value):
        self.__combat_hp[pokemon] = max(0, value)

    def reduce_hp(self, pokemon, damage):
        current = self.get_combat_hp(pokemon)
        self.set_combat_hp(pokemon, current - damage)

    def exe_at(self, atk, dfd, move):
        """Execute an attack: run the engine and apply damage."""
        print(f"\n{atk._name} used {move.name}!")

        atk_moves = []
        dfd_moves = []

        engine = CombatEngine(
            atk=atk,
            dfd=dfd,
            move=move,
            atk_moves=atk_moves,
            dfd_moves=dfd_moves
        )

        damage, was_critical = engine.calculate_damage()

        if damage == 0:
            print("The attack missed!")
            return

        self.reduce_hp(dfd, damage)

        print(f"It dealt {damage} damage!")

        if was_critical:
            print("A critical hit!")

        print(dfd.receive_attack(move.type))

    def resolve_turn(self, action1, action2):

        if action1["action"] == "surrender":
            print(f"{self.trainer1.name} surrendered!")
            print(f"{self.trainer2.name} won the battle!")
            return False

        if action2["action"] == "surrender":
            print(f"{self.trainer2.name} surrendered!")
            print(f"{self.trainer1.name} won the battle!")
            return False

        if action1["action"] == "switch" and action2["action"] == "switch":
            self.__active1 = action1["new_pokemon"]
            print(f"{self.trainer1.name} sent out {self.__active1._name}!")

            self.__active2 = action2["new_pokemon"]
            print(f"{self.trainer2.name} sent out {self.__active2._name}!")
            return True

        elif action1["action"] == "switch":
            self.__active1 = action1["new_pokemon"]
            print(f"\n{self.trainer1.name} sent out {self.__active1._name}!")

            if action2["action"] == "attack":
                self.exe_at(self.__active2, self.__active1, action2["move"])
            return True

        elif action2["action"] == "switch":
            self.__active2 = action2["new_pokemon"]
            print(f"\n{self.trainer2.name} sent out {self.__active2._name}!")

            if action1["action"] == "attack":
                self.exe_at(self.__active1, self.__active2, action1["move"])
            return True

        if action1["action"] == "attack" and action2["action"] == "attack":
            if self.__active1.get_stats().speed >= self.__active2.get_stats().speed:
                print(f"\n{self.__active1._name} is faster!")

                self.exe_at(self.__active1, self.__active2, action1["move"])

                if self.get_combat_hp(self.__active2) > 0:
                    self.exe_at(self.__active2, self.__active1, action2["move"])
            else:
                print(f"\n{self.__active2._name} is faster!")

                self.exe_at(self.__active2, self.__active1, action2["move"])

                if self.get_combat_hp(self.__active1) > 0:
                    self.exe_at(self.__active1, self.__active2, action1["move"])

            return True
        return True

    def combat(self):
        """Main loop for the battle until one trainer runs out of Pokémon."""
        print(60 * "=")
        print(f"{self.trainer1.name} VS {self.trainer2.name}")
        print(60 * "=")

        while len(self.__team1) > 0 and len(self.__team2) > 0:
            self.__number_turn += 1
            print("\n" + 60 * "=")
            print(f"TURN #{self.__number_turn}")
            print(60 * "=")

            action1 = self.player_turn(self.trainer1, self.__active1, self.__active2)
            action2 = self.player_turn(self.trainer2, self.__active2, self.__active1)

            if not self.resolve_turn(action1, action2):
                return

            if self.get_combat_hp(self.__active1) <= 0:
                print(f"{self.__active1._name} was defeated!")
                self.__team1.remove(self.__active1)

                if len(self.__team1) > 0:
                    print(f"{self.trainer1.name} must choose another Pokémon:")
                    self.__active1 = self.set_active1()
                else:
                    print(f"\n🎉 {self.trainer2.name} wins the battle!")
                    print(f"{self.trainer1.name} has no Pokémon left!")
                    return

            if self.get_combat_hp(self.__active2) <= 0:
                print(f"{self.__active2._name} was defeated!")
                self.__team2.remove(self.__active2)

                if len(self.__team2) > 0:
                    print(f"\n{self.trainer2.name} must choose another Pokémon:")
                    self.__active2 = self.set_active2()
                else:
                    print(f"\n🎉 {self.trainer1.name} wins the battle!")
                    print(f"{self.trainer2.name} has no Pokémon left!")
                    return
