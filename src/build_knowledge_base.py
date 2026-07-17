from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "fighter_details.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "fighter_docs"


def safe_value(value, fallback="Unknown"):
    """Return a readable fallback for missing dataset values."""
    if pd.isna(value):
        return fallback
    return value


def format_percentage(value):
    """Format percentage values stored as whole numbers."""
    if pd.isna(value):
        return "Unknown"
    return f"{float(value):.1f}%"


def format_number(value, decimals=2):
    """Format numeric values consistently."""
    if pd.isna(value):
        return "Unknown"
    return f"{float(value):.{decimals}f}"


def build_fighter_document(row):
    name = safe_value(row["name"])
    nickname = safe_value(row["nick_name"], fallback="None listed")
    stance = safe_value(row["stance"])
    date_of_birth = safe_value(row["dob"])

    record = (
        f"{int(row['wins'])}-{int(row['losses'])}-{int(row['draws'])}"
        if not any(pd.isna(row[col]) for col in ["wins", "losses", "draws"])
        else "Unknown"
    )

    document = f"""
Fighter Profile: {name}

Identity
Name: {name}
Nickname: {nickname}
Professional Record: {record}
Stance: {stance}
Date of Birth: {date_of_birth}

Physical Attributes
Height: {format_number(row['height'])} cm
Weight: {format_number(row['weight'])} kg
Reach: {format_number(row['reach'])} cm

Striking Statistics
Significant Strikes Landed per Minute: {format_number(row['splm'])}
Significant Striking Accuracy: {format_percentage(row['str_acc'])}
Significant Strikes Absorbed per Minute: {format_number(row['sapm'])}
Significant Strike Defence: {format_percentage(row['str_def'])}

Grappling Statistics
Average Takedowns Landed per 15 Minutes: {format_number(row['td_avg'])}
Takedown Accuracy: {format_percentage(row['td_avg_acc'])}
Takedown Defence: {format_percentage(row['td_def'])}
Average Submission Attempts per 15 Minutes: {format_number(row['sub_avg'])}

Data Note
This profile is generated from structured historical fighter statistics.
The statistics describe recorded performance and should not be treated as a complete account of current form, strategy, injuries, or recent development.
""".strip()

    return document


def make_filename(name):
    """Create a filesystem-safe fighter filename."""
    cleaned = "".join(
        character.lower() if character.isalnum() else "_"
        for character in name
    )
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return f"{cleaned}.txt"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fighters = pd.read_csv(INPUT_FILE)

    required_columns = {
        "name",
        "nick_name",
        "wins",
        "losses",
        "draws",
        "height",
        "weight",
        "reach",
        "stance",
        "dob",
        "splm",
        "str_acc",
        "sapm",
        "str_def",
        "td_avg",
        "td_avg_acc",
        "td_def",
        "sub_avg",
    }

    missing_columns = required_columns.difference(fighters.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    created = 0

    for _, fighter in fighters.iterrows():
        name = fighter["name"]

        if pd.isna(name):
            continue

        document = build_fighter_document(fighter)
        output_path = OUTPUT_DIR / make_filename(str(name))
        output_path.write_text(document, encoding="utf-8")
        created += 1

    print(f"Created {created} fighter documents.")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()