from pokemon import Pokemon

if __name__ == "__main__":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass",
        "blue",
        "male"
    )
    print(bulbasaur)
    bulbasaur.attack()
