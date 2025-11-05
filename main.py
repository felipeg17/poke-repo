from pokemon import Pokemon

if __name__ == "__main__":
    bulbasaur = Pokemon(
        pokemon_name="bulbasaur",
        pokedex_num=1,
        type="grass",
        color="blue",
        sex="male",
        level=15,
    )
    print(bulbasaur)
    print(bulbasaur.get_attribute("stats"))
    bulbasaur.level_up()
    print(bulbasaur.get_attribute("stats"))
    bulbasaur.show_moves()
