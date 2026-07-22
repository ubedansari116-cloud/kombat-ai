from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGHTS_PATH = PROJECT_ROOT / "data" / "fight_details.csv"
from fighter_repository import FighterRepository

class FightHistory:

    def __init__(self):

        fights = pd.read_csv(FIGHTS_PATH)

        events = pd.read_csv(
            PROJECT_ROOT / "data" / "event_details.csv"
        )

        events["date"] = pd.to_datetime(events["date"])

        self.df = fights.merge(
            events[["fight_id", "date"]],
            on="fight_id",
            how="left",
        )

        self.repository = FighterRepository()
    
    def build_snapshot(self, fight, fighter_name):

        profile = self.repository.get_fighter(fighter_name)

        if profile is None:
            return None

        stats = profile["stats"].copy()

        if fight["r_name"] == fighter_name:
            prefix = "r_"
            opponent_prefix = "b_"
            opponent = fight["b_name"]
        else:
            prefix = "b_"
            opponent_prefix = "r_"
            opponent = fight["r_name"]

        strike_accuracy = []
        strike_defense = []

        takedown_accuracy = []
        takedown_defense = []

        str_acc = pd.to_numeric(
            fight[f"{prefix}sig_str_acc"],
            errors="coerce",
        )

        opp_str_acc = pd.to_numeric(
            fight[f"{opponent_prefix}sig_str_acc"],
            errors="coerce",
        )

        td_acc = pd.to_numeric(
            fight[f"{prefix}td_acc"],
            errors="coerce",
        )

        opp_td_acc = pd.to_numeric(
            fight[f"{opponent_prefix}td_acc"],
            errors="coerce",
        )

        if pd.notna(str_acc):
            strike_accuracy.append(str_acc)

        if pd.notna(opp_str_acc):
            strike_defense.append(100 - opp_str_acc)

        if pd.notna(td_acc):
            takedown_accuracy.append(td_acc)

        if pd.notna(opp_td_acc):
            takedown_defense.append(100 - opp_td_acc)

        stats["striking_accuracy"] = self.safe_mean(strike_accuracy)

        stats["strike_defense"] = self.safe_mean(strike_defense)

        stats["takedown_accuracy"] = self.safe_mean(takedown_accuracy)

        stats["takedown_defense"] = self.safe_mean(takedown_defense)

        return {

            "fighter": fighter_name,

            "event": fight["event_name"],

            "fight_id": fight["fight_id"],

            "opponent": opponent,

            "division": fight["division"],

            "title_fight": fight["title_fight"],

            "method": fight["method"],

            "stats": stats,
        }

    def get_current(self, fighter_name):

        fights = self.df[
            (self.df["r_name"] == fighter_name)
            | (self.df["b_name"] == fighter_name)
        ].copy()

        if fights.empty:
            return None
        

        fights = fights.sort_values("date")

        fight = fights.iloc[-1]

        return self.build_snapshot(fight, fighter_name)

    def get_debut(self, fighter_name):

        fights = self.df[
            (self.df["r_name"] == fighter_name)
            | (self.df["b_name"] == fighter_name)
        ].copy()

        fights = fights.sort_values("date")

        if fights.empty:
            return None

        fight = fights.iloc[0]

        return self.build_snapshot(fight, fighter_name)
           
    def performance_score(self, fight, prefix):

        opponent = "b_" if prefix == "r_" else "r_"

        def value(column):
            x = fight.get(column)

            if pd.isna(x):
                return 0.0

            return float(x)

        strike_defense = (
            100 - value(f"{opponent}sig_str_acc")
        )

        takedown_defense = (
            100 - value(f"{opponent}td_acc")
        )

        score = (

            value(f"{prefix}sig_str_acc") * 0.30 +

            strike_defense * 0.25 +

            value(f"{prefix}td_acc") * 0.20 +

            takedown_defense * 0.15 +

            value(f"{prefix}kd") * 5 +

            value(f"{prefix}sub_att") * 2 +

            value(f"{prefix}td_landed") * 1

        )

        return round(score, 2)
    
    def classify_pair(self, pair_scores, peak_score):

        if len(pair_scores) == 0:
            return "LOW"

        average = sum(pair_scores) / len(pair_scores)

        ratio = average / peak_score

        if ratio >= 0.90:
            return "HIGH"

        elif ratio >= 0.75:
            return "MEDIUM"

        return "LOW"
    
    def build_prime_run(self, fights, fighter_name):

        fights = fights.sort_values("date").reset_index(drop=True)

        performance_scores = []

        for _, fight in fights.iterrows():

            prefix = "r_" if fight["r_name"] == fighter_name else "b_"

            performance_scores.append(
                self.performance_score(fight, prefix)
            )

        fights["performance_score"] = performance_scores

        peak_index = int(
            fights["performance_score"].to_numpy().argmax()
        )

        prime_indices = {peak_index}

        # =========================
        # LEFT SIDE
        # =========================

        i = peak_index - 2

        while i >= 0:

            pair = fights.iloc[i:i+2]

            result = self.classify_pair(
                pair["performance_score"].tolist(),
                fights.iloc[peak_index]["performance_score"],
            )

            if result == "HIGH":

                prime_indices.update(pair.index.tolist())
                i -= 2
                continue

            elif result == "MEDIUM":

                prime_indices.update(pair.index.tolist())
                break

            else:
                break

        # =========================
        # RIGHT SIDE
        # =========================

        i = peak_index + 1

        while i < len(fights):

            pair = fights.iloc[i:i+2]

            if pair.empty:
                break

            result = self.classify_pair(
                pair["performance_score"].tolist(),
                fights.iloc[peak_index]["performance_score"],
            )

            if result == "HIGH":

                prime_indices.update(pair.index.tolist())
                i += 2
                continue

            elif result == "MEDIUM":

                prime_indices.update(pair.index.tolist())
                break

            else:
                break

        prime_indices = sorted(prime_indices)

        return fights.iloc[prime_indices].reset_index(drop=True)
    
    def safe_mean(self, values):

        if not values:
            return 0.0

        return round(float(pd.Series(values).mean()), 1)
    
    def build_prime_snapshot(self, prime_fights, fighter_name):

        profile = self.repository.get_fighter(fighter_name)

        if profile is None:
            return None

        stats = profile["stats"].copy()

        opponent_prefix = []

        strike_accuracy = []
        strike_defense = []

        takedown_accuracy = []
        takedown_defense = []

        for _, fight in prime_fights.iterrows():

            if fight["r_name"] == fighter_name:

                prefix = "r_"
                opponent = "b_"

            else:

                prefix = "b_"
                opponent = "r_"

            strike_acc = pd.to_numeric(
                fight[f"{prefix}sig_str_acc"],
                errors="coerce",
            )

            opp_str_acc = pd.to_numeric(
                fight[f"{opponent}sig_str_acc"],
                errors="coerce",
            )

            td_acc = pd.to_numeric(
                fight[f"{prefix}td_acc"],
                errors="coerce",
            )

            opp_td_acc = pd.to_numeric(
                fight[f"{opponent}td_acc"],
                errors="coerce",
            )

            if pd.notna(strike_acc):
                strike_accuracy.append(strike_acc)

            if pd.notna(opp_str_acc):
                strike_defense.append(100 - opp_str_acc)

            if pd.notna(td_acc):
                takedown_accuracy.append(td_acc)

            if pd.notna(opp_td_acc):
                takedown_defense.append(100 - opp_td_acc)

        stats["striking_accuracy"] = self.safe_mean(strike_accuracy)

        stats["strike_defense"] = self.safe_mean(strike_defense)

        stats["takedown_accuracy"] = self.safe_mean(takedown_accuracy)

        stats["takedown_defense"] = self.safe_mean(takedown_defense)

        return {
            "fighter": fighter_name,
            "event": "Prime Career",
            "fight_id": None,
            "opponent": "Composite",
            "division": prime_fights["division"].mode().iloc[0],
            "title_fight": False,
            "method": "Composite",
            "stats": stats,
        }
    
    def get_prime(self, fighter_name):

        fights = self.df[
            (self.df["r_name"] == fighter_name)
            | (self.df["b_name"] == fighter_name)
        ].copy()

        if fights.empty:
            return None

        prime_fights = self.build_prime_run(
            fights,
            fighter_name,
        )

        return self.build_prime_snapshot(
            prime_fights,
            fighter_name,
        )
    

    def get_top_fights(self, fighter_name):
        pass