class ConfidenceEngine:

    def calculate(
        self,
        result,
        stats_one,
        stats_two,
    ):

        # ----------------------------
        # Layer 1 : Probability Gap
        # ----------------------------

        p1 = float(result["fighter_one_probability"])
        p2 = float(result["fighter_two_probability"])

        gap = abs(p1 - p2)

        probability_score = gap * 0.40
        confidence_score = probability_score

        # ----------------------------
        # Layer 2 : Attribute Dominance
        # ----------------------------

        attribute_score = 0
        reasons = []

        comparisons = [
            ("Striking Accuracy", "striking_accuracy"),
            ("Strike Defense", "strike_defense"),
            ("Takedown Accuracy", "takedown_accuracy"),
            ("Takedown Defense", "takedown_defense"),
        ]

        winner = result["predicted_winner"]

        for label, key in comparisons:

            if winner == result["fighter_one"]:
                diff = stats_one[key] - stats_two[key]
            else:
                diff = stats_two[key] - stats_one[key]

            if diff >= 20:
                attribute_score += 7.5
                reasons.append(f"Major {label} advantage")

            elif diff >= 10:
                attribute_score += 5
                reasons.append(f"{label} advantage")

            elif diff >= 5:
                attribute_score += 2.5

            elif diff <= -10:
                attribute_score -= 3
                reasons.append(f"Opponent has superior {label.lower()}")

        confidence_score += attribute_score

        # ----------------------------
        # Clamp confidence
        # ----------------------------

        confidence_score = max(0, confidence_score)
        confidence_score = min(100, confidence_score)

        # ----------------------------
        # Confidence Tier
        # ----------------------------

        if confidence_score >= 60:
            tier = "Elite"

        elif confidence_score >= 45:
            tier = "High"

        elif confidence_score >= 30:
            tier = "Medium"

        else:
            tier = "Low"

        return {
            "score": round(confidence_score, 1),
            "tier": tier,
            "reasons": [
                f"Probability gap: {gap:.1f}%"
            ] + reasons,
        }