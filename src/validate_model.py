import csv
from pathlib import Path

from rag_advisor import KombatAdvisor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "model_validation.csv"

MATCHUPS = [
    ("Islam Makhachev", "Charles Oliveira"),
    ("Islam Makhachev", "Ilia Topuria"),
    ("Jon Jones", "Tom Aspinall"),
    ("Dricus du Plessis", "Khamzat Chimaev"),
    ("Merab Dvalishvili", "Sean O'Malley"),
    ("Alexander Volkanovski", "Ilia Topuria"),
    ("Belal Muhammad", "Leon Edwards"),
    ("Petr Yan", "Umar Nurmagomedov"),
    ("Alex Pereira", "Tom Aspinall"),
    ("Charles Oliveira", "Arman Tsarukyan"),
]


def probability_for(prediction, fighter_name):
    if prediction["fighter_one"] == fighter_name:
        return prediction["fighter_one_probability"]

    if prediction["fighter_two"] == fighter_name:
        return prediction["fighter_two_probability"]

    return None


def run_matchup(advisor, fighter_one, fighter_two):
    query = f"Compare {fighter_one} and {fighter_two}"
    response = advisor.answer(query)

    retrieved = [fighter["fighter"] for fighter in response["fighters"]]
    expected = {fighter_one, fighter_two}
    retrieval_ok = set(retrieved) == expected

    prediction = response.get("prediction")

    if not prediction:
        return {
            "query": query,
            "retrieved_fighter_one": retrieved[0] if retrieved else None,
            "retrieved_fighter_two": retrieved[1] if len(retrieved) > 1 else None,
            "retrieval_ok": retrieval_ok,
            "predicted_winner": None,
            "fighter_one_probability": None,
            "fighter_two_probability": None,
            "summary": response.get("summary"),
        }

    return {
        "query": query,
        "retrieved_fighter_one": retrieved[0],
        "retrieved_fighter_two": retrieved[1],
        "retrieval_ok": retrieval_ok,
        "predicted_winner": prediction["predicted_winner"],
        "fighter_one_probability": probability_for(
            prediction,
            fighter_one,
        ),
        "fighter_two_probability": probability_for(
            prediction,
            fighter_two,
        ),
        "summary": response.get("summary"),
    }


def main():
    advisor = KombatAdvisor()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    print("\nKOMBAT AI MODEL VALIDATION")
    print("=" * 90)

    for index, (fighter_one, fighter_two) in enumerate(MATCHUPS, start=1):
        forward = run_matchup(advisor, fighter_one, fighter_two)
        reverse = run_matchup(advisor, fighter_two, fighter_one)

        forward_probability = forward["fighter_one_probability"]
        reverse_probability = reverse["fighter_two_probability"]

        if forward_probability is not None and reverse_probability is not None:
            order_difference = abs(
                forward_probability - reverse_probability
            )
            order_consistent = order_difference <= 5.0
        else:
            order_difference = None
            order_consistent = False

        probabilities = [
            value
            for value in [
                forward["fighter_one_probability"],
                forward["fighter_two_probability"],
            ]
            if value is not None
        ]

        extreme_probability = (
            bool(probabilities)
            and max(probabilities) >= 90.0
        )

        row = {
            "matchup": f"{fighter_one} vs {fighter_two}",
            "retrieval_ok": forward["retrieval_ok"],
            "retrieved_fighter_one": forward["retrieved_fighter_one"],
            "retrieved_fighter_two": forward["retrieved_fighter_two"],
            "predicted_winner": forward["predicted_winner"],
            f"{fighter_one}_probability": forward["fighter_one_probability"],
            f"{fighter_two}_probability": forward["fighter_two_probability"],
            "reverse_order_probability_for_first_fighter": reverse_probability,
            "order_difference": (
                round(order_difference, 2)
                if order_difference is not None
                else None
            ),
            "order_consistent_within_5_points": order_consistent,
            "extreme_probability_90_plus": extreme_probability,
            "manual_eye_test": "",
            "notes": "",
        }
        rows.append(row)

        print(f"\n{index}. {fighter_one} vs {fighter_two}")
        print("-" * 90)
        print(
            f"Retrieved: {forward['retrieved_fighter_one']} vs "
            f"{forward['retrieved_fighter_two']}"
        )
        print(f"Retrieval correct: {forward['retrieval_ok']}")
        print(
            f"Prediction: {forward['predicted_winner']} | "
            f"{fighter_one}: {forward['fighter_one_probability']}% | "
            f"{fighter_two}: {forward['fighter_two_probability']}%"
        )
        print(
            f"Order consistency difference: "
            f"{row['order_difference']} percentage points"
        )
        print(
            f"Order consistent: "
            f"{row['order_consistent_within_5_points']}"
        )
        print(f"Extreme probability: {extreme_probability}")

    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    retrieval_passes = sum(row["retrieval_ok"] for row in rows)
    order_passes = sum(
        row["order_consistent_within_5_points"]
        for row in rows
    )
    extreme_count = sum(
        row["extreme_probability_90_plus"]
        for row in rows
    )

    print("\n" + "=" * 90)
    print("VALIDATION SUMMARY")
    print("=" * 90)
    print(f"Retrieval checks passed: {retrieval_passes}/{len(rows)}")
    print(f"Order checks passed: {order_passes}/{len(rows)}")
    print(f"Extreme predictions: {extreme_count}/{len(rows)}")
    print(f"CSV saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
