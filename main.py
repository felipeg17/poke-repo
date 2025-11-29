from pokemon import Pokemon
from combat.field import Battle, Field, Trainer

if __name__ == "__main__":
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        pokedex_num=1,
        type="Grass",
        color="blue",
        sex="male",
        level=15,
    )
    print(bulbasaur)
    print(bulbasaur.get_attribute("stats"))
    bulbasaur.level_up()
    print(bulbasaur.get_attribute("stats"))
    bulbasaur.show_moves()

    """Main game loop with restart menu"""
    print("=" * 60)
    print("POKÉMON BATTLE SIMULATOR")
    print("=" * 60)

    while True:
        print("\n" + "=" * 60)
        trainer1_name = input("Trainer 1 name: ")
        trainer2_name = input("Trainer 2 name: ")
        trainer1 = Trainer(trainer1_name)
        trainer2 = Trainer(trainer2_name)

        print("\n" + "=" * 60)
        trainer1.choose_pokemon()

        print("\n" + "=" * 60)
        trainer2.choose_pokemon()

        print("\n" + "=" * 60)
        print("BATTLE START!")
        print("=" * 60)
        field = Field(trainer1, trainer2)
        batalla = Battle(field)
        batalla.battle()

        print("\n" + "=" * 60)
        print("BATTLE END")
        print("=" * 60)

        while True:
            option = input(
                "\nWhat do you want to do?\n(1) Play again\n(2) Exit\n> "
            ).strip()

            if option == "1":
                print("\n" + "=" * 60)
                print("NEW BATTLE")
                print("=" * 60)
                break
            elif option == "2":
                print("\nThanks for playing! See you later!")
                break
            else:
                print("Invalid option. Choose 1 or 2.")
        if option == "2":
            break
