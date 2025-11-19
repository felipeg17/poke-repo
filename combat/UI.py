from field import Field, Trainer
from pokemon import Pokemon, Move


class BattleUI:
    """All user interaction for battles"""
    
    def __init__(self, field: Field):
        self.field = field
    
    def display_battle_header(self):
    
        print(60 * "=")
        print(f"{self.field.trainer1.name} VS {self.field.trainer2.name}")
        print(60 * "=")
    
    def display_turn_header(self):
        print("\n" + 60 * "=")
        print(f"TURN #{self.field.get_turn_number() + 1}")
        print(60 * "=")
    
    def display_battle_status(self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon):
        
        active_hp = self.field.get_combat_hp(active_pokemon)
        enemy_hp = self.field.get_combat_hp(enemy_pokemon)
        
        print(f"""
        {50 * "="}
        Turn: {trainer.name}
        {active_pokemon._name:<20} VS {enemy_pokemon._name:>20}
        {self.field.health_bar(active_hp, active_pokemon._stats.hp)}  {self.field.health_bar(enemy_hp, enemy_pokemon._stats.hp)}
        {50 * "="}
        """)
    
    def action_py(self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon):
        self.display_battle_status(trainer, active_pokemon, enemy_pokemon)
        
        choice = int(input("""
              (1) Attack
              (2) Switch Pokémon
              (0) Surrender
              """))
        
        if choice == 1:
            return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
        elif choice == 2:
            return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
        elif choice == 0:
            return self.choice_surrender(trainer)
        else:
            print("Invalid choice. Try again.")
            return self.action_py(trainer, active_pokemon, enemy_pokemon)
    
    def choice_attack(self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon):
        moves = active_pokemon.get_moveset().current_moves
        
        print(f"\n{30 * '='}")
        print(" Attacks:")
        for i, move in enumerate(moves, 1):
            print(f"({i}) {move}")
        print(f"{30 * '='}")
        
        try:
            choice_move = int(input("Choose (0 to go back): "))
            if choice_move == 0:
                return self.action_py(trainer, active_pokemon, enemy_pokemon)
            elif 1 <= choice_move <= len(moves):
                chosen_move = moves[choice_move - 1]
                print(f"{active_pokemon._name} will use {chosen_move.name}!")
                return {"action": "attack", "move": chosen_move}
            else:
                print("Invalid choice.")
                return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
        except ValueError:
            print("Enter a valid number.")
            return self.choice_attack(trainer, active_pokemon, enemy_pokemon)
    
    def choice_switch(self, trainer: Trainer, active_pokemon: Pokemon, enemy_pokemon: Pokemon):
        team = trainer.pokemon
        print(f"{30 * '='}")
        print("Your team:")
        
        for i, pokemon in enumerate(team, 1):
            current_hp = self.field.get_combat_hp(pokemon)
            max_hp = pokemon._stats.hp
            hp_bar = self.field.health_bar(current_hp, max_hp, bar_length=15)
            
            if pokemon == active_pokemon:
                status = " - (Active)"
            elif current_hp <= 0:
                status = " (defeated)"
            else:
                status = ""
            
            print(f"({i}) {pokemon._name} {hp_bar}{status}")
        print(f"{30 * '='}")
        
        try:
            choice_pkm = int(input("\nChoose a Pokémon (0 to go back): "))
            
            if choice_pkm == 0:
                return self.action_py(trainer, active_pokemon, enemy_pokemon)
            elif 1 <= choice_pkm <= len(team):
                new_pokemon = team[choice_pkm - 1]
                
                if new_pokemon == active_pokemon:
                    print("That Pokémon is already in battle!")
                    return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
                elif self.field.get_combat_hp(new_pokemon) <= 0:
                    print("That Pokémon has been defeated!")
                    return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
                else:
                    print(f"Go, {new_pokemon._name}!")
                    return {"action": "switch", "new_pokemon": new_pokemon}
            else:
                print("Invalid option.")
                return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
        except ValueError:
            print("Enter a valid number.")
            return self.choice_switch(trainer, active_pokemon, enemy_pokemon)
    
    def choice_surrender(self, trainer: Trainer):
    
        confirm = input(f"Are you sure you want to surrender, {trainer.name}? (y/n) ")
        if confirm.lower() == 'y':
            return {"action": "surrender"}
        else:
            return self.action_py(
                trainer, 
                self.field.get_active1() if trainer == self.field.trainer1 else self.field.get_active2(),
                self.field.get_active2() if trainer == self.field.trainer1 else self.field.get_active1()
            )
    
    def choice_switch(self, trainer: Trainer):
        
        print(f"\n{trainer.name}, choose your next Pokémon:")
        available = self.field.pokemon_available(trainer)
        
        for i, pokemon in enumerate(available, 1):
            current_hp = self.field.get_combat_hp(pokemon)
            max_hp = pokemon._stats.hp
            hp_bar = self.field.health_bar(current_hp, max_hp, bar_length=15)
            print(f"({i}) {pokemon._name} {hp_bar}")
        
        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(available):
                    new_pokemon = available[choice]
                    print(f"Go, {new_pokemon._name}!")
                    self.field.switch_pokemon(trainer, new_pokemon)
                    return new_pokemon
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Enter a valid number.")
    
    def display_messages(self, messages):
        for msg in messages:
            print(msg)
    
    def battle(self):
        """Main battle"""
        self.display_battle_header()
        
        while not self.field.end_battle():
            self.display_turn_header()
            

            action1 = self.action_py(
                self.field.trainer1, 
                self.field.get_active1(), 
                self.field.get_active2()
            )
            
            action2 = self.action_py(
                self.field.trainer2, 
                self.field.get_active2(), 
                self.field.get_active1()
            )
            
            
            continue_battle, messages = self.field.resolve_turn(action1, action2)
            self.display_messages(messages)
            
            if not continue_battle:
                break
            
    
            needs_switch1, needs_switch2, defeated_messages = self.field.remove_defeated_pokemon()
            self.display_messages(defeated_messages)
            
            if self.field.end_battle():
                break
            
            if needs_switch1:
                self.choice_switch(self.field.trainer1)
            
            if needs_switch2:
                self.choice_switch(self.field.trainer2)
        
        
        winner = self.field.winner_game()
        if winner:
            print(f"\n🎉 {winner.name} is the winner!")
