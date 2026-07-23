import random

class ExplainabilityEngine:

    def get_matchup_context(
        self,
        result,
        stats_one,
        stats_two,
        fighter_one,
        fighter_two,
    ):

        winner = result["predicted_winner"]

        if winner == fighter_one:

            return {
                "winner": fighter_one,
                "loser": fighter_two,
                "winner_stats": stats_one,
                "loser_stats": stats_two,
            }

        return {
            "winner": fighter_two,
            "loser": fighter_one,
            "winner_stats": stats_two,
            "loser_stats": stats_one,
        }
    
    def build_paragraph(
        self,
        context,
        advantages,
    ):

        winner = context["winner"]
        loser = context["loser"]

        if len(advantages) == 0:

            return (
                f"This projects as an extremely competitive matchup. "
                f"{winner} receives only a slight statistical edge over "
                f"{loser}, making this one of the closest simulations."
            )

        categories = {a["category"] for a in advantages}

        phrases = []

        # Complete striking package
        if "striking" in categories and "strike_defense" in categories:

            phrases.append(
                "control striking exchanges from both an offensive and defensive standpoint"
            )

        else:

            if "striking" in categories:
                phrases.append(
                    "land the cleaner and more effective strikes"
                )

            if "strike_defense" in categories:
                phrases.append(
                    "avoid prolonged damage through superior defensive striking"
                )

        # Complete grappling package
        if "wrestling" in categories and "grappling_defense" in categories:

            phrases.append(
                "control where the fight takes place while consistently shutting down takedown attempts"
            )

        else:

            if "wrestling" in categories:
                phrases.append(
                    "dictate where the fight takes place through dominant wrestling"
                )

            if "grappling_defense" in categories:
                phrases.append(
                    "consistently shut down takedown attempts"
                )

        if len(phrases) == 1:

            body = phrases[0]

        elif len(phrases) == 2:

            body = f"{phrases[0]} while also {phrases[1]}"

        else:

            body = ", ".join(phrases[:-1]) + f", and {phrases[-1]}"

        openings = [

            f"{winner} is projected to win because",

            f"The model favors {winner} because",

            f"{winner} receives the statistical edge because",

            f"{winner} appears to hold the stronger overall profile because",

        ]

        opening = random.choice(openings)

        return (
            f"{opening} they are expected to "
            f"{body}. Collectively, these advantages create the clearest "
            f"path to victory while limiting {loser}'s strongest weapons."
        )
    
    
    
    def detect_advantages(self, context):

        winner = context["winner_stats"]
        loser = context["loser_stats"]

        advantages = []

        comparisons = [
            ("striking_accuracy", "striking"),
            ("strike_defense", "strike_defense"),
            ("takedown_accuracy", "wrestling"),
            ("takedown_defense", "grappling_defense"),
        ]

        for key, category in comparisons:

            diff = winner[key] - loser[key]

            if diff >= 15:

                level = "major"

            elif diff >= 8:

                level = "moderate"

            elif diff >= 4:

                level = "minor"

            else:

                continue

            advantages.append(
                {
                    "category": category,
                    "level": level,
                    "difference": round(diff, 1),
                }
            )

        return advantages

    def generate(
        self,
        result,
        stats_one,
        stats_two,
        fighter_one,
        fighter_two,
    ):

        context = self.get_matchup_context(
            result,
            stats_one,
            stats_two,
            fighter_one,
            fighter_two,
        )

        advantages = self.detect_advantages(context)

        paragraph = self.build_paragraph(
            context,
            advantages,
        )

        return paragraph