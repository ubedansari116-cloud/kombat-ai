from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "fighter_details.csv"


class FighterRepository:

    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def get_all_fighters(self):
        return sorted(self.df["name"].tolist())

    def get_fighter(self, name):

        fighter = self.df[self.df["name"] == name]

        if fighter.empty:
            return None

        row = fighter.iloc[0]

        return {

            "name": row["name"],

            "division": row.get("division", None),

            "stance": row.get("stance", None),

            "age": row.get("age", None),

            "stats": {

                "wins": int(row["wins"]),
                "losses": int(row["losses"]),

                "height": float(row["height"]),
                "weight": float(row["weight"]),
                "reach": float(row["reach"]),

                "splm": float(row["splm"]),
                "striking_accuracy": float(row["str_acc"]),
                "sapm": float(row["sapm"]),
                "strike_defense": float(row["str_def"]),

                "takedown_avg": float(row["td_avg"]),
                "takedown_accuracy": float(row["td_avg_acc"]),
                "takedown_defense": float(row["td_def"]),

                "submission_avg": float(row["sub_avg"]),
            },
        }