from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "kombat_ai_rf_v2.pkl"
FEATURES_PATH = PROJECT_ROOT / "models" / "kombat_ai_rf_v2_features.pkl"


class KombatPredictor:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        if not FEATURES_PATH.exists():
            raise FileNotFoundError(
                f"Feature list not found: {FEATURES_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)
        self.feature_columns = joblib.load(FEATURES_PATH)

    def build_feature_row(
        self,
        fighter_one_stats,
        fighter_two_stats,
        division=None,
        title_fight=False,
    ):
        required_stats = [
            "wins",
            "losses",
            "height",
            "weight",
            "reach",
            "splm",
            "striking_accuracy",
            "sapm",
            "strike_defense",
            "takedown_avg",
            "takedown_accuracy",
            "takedown_defense",
            "submission_avg",
        ]

        missing = []

        for stat in required_stats:
            if fighter_one_stats.get(stat) is None:
                missing.append(f"fighter one: {stat}")

            if fighter_two_stats.get(stat) is None:
                missing.append(f"fighter two: {stat}")

        if missing:
            raise ValueError(
                "Prediction cannot be generated because these values "
                f"are missing: {', '.join(missing)}"
            )

        differences = {
            "wins_diff":
                fighter_one_stats["wins"] - fighter_two_stats["wins"],

            "losses_diff":
                fighter_one_stats["losses"] - fighter_two_stats["losses"],

            "height_diff":
                fighter_one_stats["height"] - fighter_two_stats["height"],

            "weight_diff":
                fighter_one_stats["weight"] - fighter_two_stats["weight"],

            "reach_diff":
                fighter_one_stats["reach"] - fighter_two_stats["reach"],

            "splm_diff":
                fighter_one_stats["splm"] - fighter_two_stats["splm"],

            "str_acc_diff":
                fighter_one_stats["striking_accuracy"]
                - fighter_two_stats["striking_accuracy"],

            "sapm_diff":
                fighter_one_stats["sapm"] - fighter_two_stats["sapm"],

            "str_def_diff":
                fighter_one_stats["strike_defense"]
                - fighter_two_stats["strike_defense"],

            "td_avg_diff":
                fighter_one_stats["takedown_avg"]
                - fighter_two_stats["takedown_avg"],

            "td_acc_diff":
                fighter_one_stats["takedown_accuracy"]
                - fighter_two_stats["takedown_accuracy"],

            "td_def_diff":
                fighter_one_stats["takedown_defense"]
                - fighter_two_stats["takedown_defense"],

            "sub_avg_diff":
                fighter_one_stats["submission_avg"]
                - fighter_two_stats["submission_avg"],
        }

        feature_row = {
            feature: 0.0
            for feature in self.feature_columns
        }

        feature_row.update(differences)
        feature_row["title_fight"] = int(bool(title_fight))

        if division:
            normalized_division = division.strip().lower()
            division_column = f"division_{normalized_division}"

            if division_column in feature_row:
                feature_row[division_column] = 1.0

        return pd.DataFrame(
            [feature_row],
            columns=self.feature_columns,
        )

    def predict(
        self,
        fighter_one_name,
        fighter_one_stats,
        fighter_two_name,
        fighter_two_stats,
        division=None,
        title_fight=False,
    ):
        features = self.build_feature_row(
            fighter_one_stats=fighter_one_stats,
            fighter_two_stats=fighter_two_stats,
            division=division,
            title_fight=title_fight,
        )

        probabilities = self.model.predict_proba(features)[0]
        model_classes = list(self.model.classes_)

        fighter_one_index = model_classes.index(1)
        fighter_one_probability = float(
            probabilities[fighter_one_index] * 100
        )
        fighter_two_probability = 100.0 - fighter_one_probability

        predicted_winner = (
            fighter_one_name
            if fighter_one_probability >= fighter_two_probability
            else fighter_two_name
        )

        return {
            "fighter_one": fighter_one_name,
            "fighter_two": fighter_two_name,
            "fighter_one_probability": round(
                fighter_one_probability,
                2,
            ),
            "fighter_two_probability": round(
                fighter_two_probability,
                2,
            ),
            "predicted_winner": predicted_winner,
        }
