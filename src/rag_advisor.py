import re

from rag_retriever import FighterRetriever


class KombatAdvisor:
    def __init__(self):
        self.retriever = FighterRetriever()

    def extract_stats(self, document):
        patterns = {
            "striking_accuracy":
                r"Significant Striking Accuracy:\s*([\d.]+)",

            "strike_defense":
                r"Significant Strike Defence:\s*([\d.]+)",

            "takedown_avg":
                r"Average Takedowns Landed per 15 Minutes:\s*([\d.]+)",

            "takedown_accuracy":
                r"Takedown Accuracy:\s*([\d.]+)",

            "takedown_defense":
                r"Takedown Defence:\s*([\d.]+)",

            "submission_avg":
                r"Average Submission Attempts per 15 Minutes:\s*([\d.]+)",
        }

        stats = {}

        for stat_name, pattern in patterns.items():
            match = re.search(pattern, document)

            if match:
                stats[stat_name] = float(match.group(1))
            else:
                stats[stat_name] = None

        return stats

    def compare_fighters(self, fighter_one, fighter_two):
        stats_one = fighter_one["stats"]
        stats_two = fighter_two["stats"]

        metric_labels = {
            "striking_accuracy": "Striking Accuracy",
            "strike_defense": "Strike Defence",
            "takedown_avg": "Takedowns per 15 Minutes",
            "takedown_accuracy": "Takedown Accuracy",
            "takedown_defense": "Takedown Defence",
            "submission_avg": "Submission Attempts per 15 Minutes",
        }

        advantages = []

        fighter_one_wins = 0
        fighter_two_wins = 0
        ties = 0

        for metric, label in metric_labels.items():
            value_one = stats_one.get(metric)
            value_two = stats_two.get(metric)

            if value_one is None or value_two is None:
                winner = "Data unavailable"

            elif value_one > value_two:
                winner = fighter_one["fighter"]
                fighter_one_wins += 1

            elif value_two > value_one:
                winner = fighter_two["fighter"]
                fighter_two_wins += 1

            else:
                winner = "Tie"
                ties += 1

            advantages.append(
                {
                    "metric": label,
                    "fighter_one_value": value_one,
                    "fighter_two_value": value_two,
                    "winner": winner,
                }
            )

        if fighter_one_wins > fighter_two_wins:
            overall_edge = fighter_one["fighter"]

        elif fighter_two_wins > fighter_one_wins:
            overall_edge = fighter_two["fighter"]

        else:
            overall_edge = "Even"

        return {
            "advantages": advantages,
            "fighter_one_wins": fighter_one_wins,
            "fighter_two_wins": fighter_two_wins,
            "ties": ties,
            "overall_edge": overall_edge,
        }
    
    def generate_summary(self, fighter_one, fighter_two, comparison):
        summary_lines = []

        overall_edge = comparison["overall_edge"]

        if overall_edge != "Even":
            summary_lines.append(
                f"{overall_edge} holds the overall statistical edge."
            )

        metric_winners = {}

        for advantage in comparison["advantages"]:
            winner = advantage["winner"]

            if winner in {
                fighter_one["fighter"],
                fighter_two["fighter"],
            }:
                metric_winners.setdefault(winner, []).append(
                    advantage["metric"]
                )

        for fighter, metrics in metric_winners.items():
            metric_text = ", ".join(metrics)

            summary_lines.append(
                f"{fighter} leads in {metric_text}."
            )

        return " ".join(summary_lines)
    
    def answer(self, query):
        results = self.retriever.search(query, top_k=2)

        analysis = []

        for result in results:
            analysis.append(
                {
                    "fighter": result["fighter_name"],
                    "stats": self.extract_stats(
                        result["document"]
                    ),
                }
            )

        if len(analysis) == 2:
            comparison = self.compare_fighters(
                analysis[0],
                analysis[1],
            )

            summary = self.generate_summary(
               analysis[0],
               analysis[1],
               comparison,
) 
            return {
    "fighters": analysis,
    "comparison": comparison,
    "summary": summary,
}

        return {
            "fighters": analysis,
            "comparison": None,
        }


def print_response(response):
    print("\nRESULTS")
    print("=" * 80)

    for fighter in response["fighters"]:
        print(f"Fighter: {fighter['fighter']}")
        print("-" * 80)

        for stat_name, stat_value in fighter["stats"].items():
            print(f"{stat_name}: {stat_value}")

        print()

    comparison = response["comparison"]

    if comparison is None:
        return

    print("COMPARISON")
    print("=" * 80)

    for advantage in comparison["advantages"]:
        print(
            f"{advantage['metric']}: "
            f"{advantage['fighter_one_value']} vs "
            f"{advantage['fighter_two_value']} "
            f"→ {advantage['winner']}"
        )

    print("-" * 80)
    print(
        f"Metric wins: "
        f"{comparison['fighter_one_wins']} - "
        f"{comparison['fighter_two_wins']}"
    )
    print(f"Ties: {comparison['ties']}")
    print(f"Overall statistical edge: {comparison['overall_edge']}")
    print()
    print("ANALYST SUMMARY")
    print("=" * 80)
    print(response["summary"])


def main():
    advisor = KombatAdvisor()

    print("Kombat AI Advisor")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Advisor closed.")
            break

        try:
            response = advisor.answer(query)
            print_response(response)

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()