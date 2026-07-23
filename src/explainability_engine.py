class ExplainabilityEngine:

    def generate(
        self,
        result,
        stats_one,
        stats_two,
        fighter_one,
        fighter_two,
    ):

        winner = result["predicted_winner"]

        if winner == fighter_one:
            winner_stats = stats_one
            loser_stats = stats_two
            loser = fighter_two
        else:
            winner_stats = stats_two
            loser_stats = stats_one
            loser = fighter_one

        reasons = []

        # Striking

        if (
            winner_stats["striking_accuracy"]
            - loser_stats["striking_accuracy"]
        ) >= 10:

            reasons.append(
                "owns a significant striking accuracy advantage"
            )

        # Strike Defense

        if (
            winner_stats["strike_defense"]
            - loser_stats["strike_defense"]
        ) >= 10:

            reasons.append(
                "defends strikes more effectively"
            )

        # Wrestling

        if (
            winner_stats["takedown_accuracy"]
            - loser_stats["takedown_accuracy"]
        ) >= 10:

            reasons.append(
                "is expected to control grappling exchanges"
            )

        # Defensive Wrestling

        if (
            winner_stats["takedown_defense"]
            - loser_stats["takedown_defense"]
        ) >= 10:

            reasons.append(
                "can likely neutralize takedown attempts"
            )

        if len(reasons) == 0:

            return (
                f"This projects as a competitive matchup. "
                f"{winner} receives only a slight statistical edge over "
                f"{loser}, resulting in a narrow prediction."
            )

        explanation = (
            f"{winner} is favored because "
            + ", ".join(reasons[:-1])
        )

        if len(reasons) > 1:
            explanation += f", and {reasons[-1]}."

        else:
            explanation = (
                f"{winner} is favored because "
                f"{reasons[0]}."
            )

        return explanation