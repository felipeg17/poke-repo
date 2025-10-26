import pandas as pd
from pathlib import Path

class Move:
    # Represents a single Pokemon move
    def __init__(self, move_id, name, type_, power, accuracy, pp):
        self.id = move_id
        self.name = name
        self.type = type_
        self.power = power
        self.accuracy = accuracy
        self.pp = pp

    def __str__(self):
        return f"{self.name} ({self.type}) | Power: {self.power}, Accuracy: {self.accuracy}, PP: {self.pp}"


class Moveset:
    # Manages the moveset of a Pokemon based on its Pokedex number and level
    def __init__(self, pokedex_num: int, level: int):
        self.current_dir = Path(__file__).parent # Actual directory of moveset.py
        self.moves_path = self.current_dir / "utils" / "moves.csv" # Path to moves.csv
        self.pokemon_moves_path = self.current_dir / "utils" / "pokemon_moves.csv" # Path to pokemon_moves.csv

        self.pokedex_num = pokedex_num
        self.level = level
        self.available_moves = self._load_available_moves()
        self.current_moves = self._select_current_moves()

    def _load_available_moves(self):
        # Uses the CSV files to load all moves the Pokemon can learn up to its current level
        moves_df = pd.read_csv(self.moves_path) # Load moves data 
        pm_df = pd.read_csv(self.pokemon_moves_path) # Load pokemon_moves data -> moves learnable by each Pokemon

        # Filter by this Pokemon's Pokedex number
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        # Filter by level learned
        pm_df = pm_df[pm_df["level_learned"] <= self.level]

        # Merge to get full move details
        merged = pm_df.merge(moves_df, left_on="move_id", right_on="id")

        moves = [] # collect Move objects
        for i, row in merged.iterrows():
            move = Move(
                move_id=row["id"],
                name=row["name"],
                type_=row["type"],
                power=row["power"],
                accuracy=row["accuracy"],
                pp=row["pp"]
            )
            moves.append(move)
        return moves

    def _select_current_moves(self):
        # Selects up to 4 moves based on the highest level learned
        if not self.available_moves:
            return []
        # Load pokemon_moves to filter by level learned
        pm_df = pd.read_csv(self.pokemon_moves_path)
        pm_df = pm_df[pm_df["pokemon_id"] == self.pokedex_num]
        pm_df = pm_df[pm_df["level_learned"] <= self.level]
        pm_df = pm_df.sort_values(by="level_learned", ascending=False)
        top_moves_ids = pm_df["move_id"].head(4).tolist()

        # Select corresponding Move objects
        selected = []  

        for m in self.available_moves:
            # Check if the move's ID is in the top moves list
            if m.id in top_moves_ids:
                selected.append(m)

        return selected


    def show_moves(self):
        # Displays the current moves of the Pokemon
        if not self.current_moves:
            print("This Pokemon has no moves.")
            return
        for move in self.current_moves:
            print(f"- {move}")

    def get_moves_names(self):
        # Returns a list of the names of the current moves
        return [m.name for m in self.current_moves]
