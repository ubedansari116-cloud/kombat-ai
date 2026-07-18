from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "fight_details.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "fighter_heatmaps.csv"


def percentage(head, body, leg):
    total = head + body + leg

    if total == 0:
        return 0.0, 0.0, 0.0

    return (
        round(head / total * 100, 2),
        round(body / total * 100, 2),
        round(leg / total * 100, 2),
    )


fighters = {}

fights = pd.read_csv(INPUT_FILE)

for _, fight in fights.iterrows():

    red = fight["r_name"]
    blue = fight["b_name"]

    if red not in fighters:
        fighters[red] = {
            "head_off": 0,
            "body_off": 0,
            "leg_off": 0,
            "head_def": 0,
            "body_def": 0,
            "leg_def": 0,
        }

    if blue not in fighters:
        fighters[blue] = {
            "head_off": 0,
            "body_off": 0,
            "leg_off": 0,
            "head_def": 0,
            "body_def": 0,
            "leg_def": 0,
        }

    # -------------------------
    # RED OFFENSE
    # -------------------------

    fighters[red]["head_off"] += fight["r_head_landed"]
    fighters[red]["body_off"] += fight["r_body_landed"]
    fighters[red]["leg_off"] += fight["r_leg_landed"]

    # RED DEFENSE

    fighters[red]["head_def"] += fight["b_head_landed"]
    fighters[red]["body_def"] += fight["b_body_landed"]
    fighters[red]["leg_def"] += fight["b_leg_landed"]

    # -------------------------
    # BLUE OFFENSE
    # -------------------------

    fighters[blue]["head_off"] += fight["b_head_landed"]
    fighters[blue]["body_off"] += fight["b_body_landed"]
    fighters[blue]["leg_off"] += fight["b_leg_landed"]

    # BLUE DEFENSE

    fighters[blue]["head_def"] += fight["r_head_landed"]
    fighters[blue]["body_def"] += fight["r_body_landed"]
    fighters[blue]["leg_def"] += fight["r_leg_landed"]

    rows = []

for fighter, values in fighters.items():

    head_off, body_off, leg_off = percentage(
        values["head_off"],
        values["body_off"],
        values["leg_off"],
    )

    head_def, body_def, leg_def = percentage(
        values["head_def"],
        values["body_def"],
        values["leg_def"],
    )

    rows.append(
        {
            "fighter": fighter,

            "head_offense": head_off,
            "body_offense": body_off,
            "leg_offense": leg_off,

            "head_defense": head_def,
            "body_defense": body_def,
            "leg_defense": leg_def,
        }
    )

    heatmap_df = pd.DataFrame(rows)

heatmap_df = heatmap_df.sort_values("fighter")

heatmap_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print()

print("Generated")

print(len(heatmap_df))

print("fighters")

print()

print(heatmap_df.head())