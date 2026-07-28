import numpy as np
import matplotlib.pyplot as plt


class FightVisualizer:

    def __init__(self):
        self.categories = [
            "Striking",
            "Defense",
            "Wrestling",
            "Grappling",
            "Physical",
            "Experience",
        ]

    def clamp(self, value):
        return max(0, min(100, value))

    def build_attributes(self, stats):

        striking = (
            stats["striking_accuracy"] * 0.6
            + stats["splm"] * 10
            - stats["sapm"] * 5
        )

        defense = (
            stats["strike_defense"] * 0.5
            + stats["takedown_defense"] * 0.5
        )

        wrestling = (
            stats["takedown_avg"] * 15
            + stats["takedown_accuracy"]
        )

        grappling = (
            stats["submission_avg"] * 25
            + stats["takedown_avg"] * 10
        )

        physical = (
            (stats["reach"] / 200) * 60
            + (stats["height"] / 200) * 40
        )

        total_fights = stats["wins"] + stats["losses"]

        if total_fights == 0:
            experience = 50
        else:
            experience = (
                (stats["wins"] / total_fights) * 70
                + min(total_fights, 40) / 40 * 30
            )

        return [
            self.clamp(striking),
            self.clamp(defense),
            self.clamp(wrestling),
            self.clamp(grappling),
            self.clamp(physical),
            self.clamp(experience),
        ]

    # --------------------------------------------------------
    # Radar
    # --------------------------------------------------------

    def create_radar_chart(
        self,
        fighter_one_name,
        fighter_one_stats,
        fighter_two_name,
        fighter_two_stats,
    ):

        fighter_one = self.build_attributes(fighter_one_stats)
        fighter_two = self.build_attributes(fighter_two_stats)

        labels = self.categories
        num_vars = len(labels)

        angles = np.linspace(
            0,
            2 * np.pi,
            num_vars,
            endpoint=False,
        ).tolist()

        fighter_one += fighter_one[:1]
        fighter_two += fighter_two[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(
            figsize=(4.8, 5.2),
            subplot_kw=dict(polar=True),
        )

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        ax.plot(
            angles,
            fighter_one,
            color="#00B4FF",
            linewidth=3,
            label=fighter_one_name,
        )

        ax.fill(
            angles,
            fighter_one,
            color="#00B4FF",
            alpha=0.25,
        )

        ax.plot(
            angles,
            fighter_two,
            color="#FF4040",
            linewidth=3,
            label=fighter_two_name,
        )

        ax.fill(
            angles,
            fighter_two,
            color="#FF4040",
            alpha=0.25,
        )

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(
            labels,
            color="white",
            fontsize=11,
            fontweight="bold",
        )

        ax.set_ylim(0, 100)

        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(
            ["20", "40", "60", "80", "100"],
            color="gray",
            fontsize=8,
        )

        ax.grid(
            color="#444444",
            linestyle="--",
            linewidth=0.8,
        )

        ax.spines["polar"].set_color("#666666")

        legend = ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=2,
            frameon=False,
            fontsize=10,
        )

        for text in legend.get_texts():
            text.set_color("white")

        plt.tight_layout()

        return fig

    # --------------------------------------------------------
    # Attribute Comparison
    # --------------------------------------------------------

    def create_attribute_comparison(
        self,
        fighter_one_name,
        fighter_one_stats,
        fighter_two_name,
        fighter_two_stats,
    ):

        import matplotlib.pyplot as plt
        import numpy as np

        def build(stats):

            power = min(100, stats["splm"] * 18)

            accuracy = stats["striking_accuracy"]

            durability = max(
                0,
                stats["strike_defense"] * 0.55 +
                (100 - stats["sapm"] * 8) * 0.45,
            )

            wrestling = min(
                100,
                stats["takedown_avg"] * 15 +
                stats["takedown_accuracy"] * 0.6,
            )

            grappling = min(
                100,
                stats["submission_avg"] * 35,
            )

            cardio = min(
                100,
                (
                    (stats["wins"] + stats["losses"]) * 2.5 +
                    stats["strike_defense"] * 0.3
                ),
            )

            fight_iq = min(
                100,
                (
                    accuracy * 0.25 +
                    stats["strike_defense"] * 0.20 +
                    stats["takedown_accuracy"] * 0.15 +
                    stats["takedown_defense"] * 0.15 +
                    stats["splm"] * 3 -
                    stats["sapm"] * 2
                ),
            )

            return {
                "👊 Power": round(power),
                "🎯 Accuracy": round(accuracy),
                "🛡 Durability": round(durability),
                "🤼 Wrestling": round(wrestling),
                "🥋 Grappling": round(grappling),
                "❤️ Cardio": round(cardio),
                "🧠 Fight IQ": round(fight_iq),
            }

        left = build(fighter_one_stats)
        right = build(fighter_two_stats)

        labels = list(left.keys())

        left_values = np.array(list(left.values()))
        right_values = np.array(list(right.values()))

        labels = labels[::-1]
        left_values = left_values[::-1]
        right_values = right_values[::-1]

        y = np.arange(len(labels))

        fig, ax = plt.subplots(figsize=(10.5, 6))

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        # Mirror bars
        ax.barh(
            y,
            -left_values,
            height=0.58,
            color="#00B4FF",
        )

        ax.barh(
            y,
            right_values,
            height=0.58,
            color="#FF4040",
        )

        # Centre line
        ax.axvline(
            0,
            color="#555555",
            linewidth=1.4,
        )

        # Attribute labels
        for i, label in enumerate(labels):

            ax.text(
                0,
                i,
                label,
                ha="center",
                va="center",
                color="white",
                fontsize=11,
                fontweight="bold",
                bbox=dict(
                    facecolor="#111111",
                    edgecolor="none",
                    pad=2,
                ),
            )

        # Numbers
        for i in range(len(labels)):

            ax.text(
                -left_values[i]-2,
                i,
                str(left_values[i]),
                ha="right",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )

            ax.text(
                right_values[i]+2,
                i,
                str(right_values[i]),
                ha="left",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )

        # Winner outline
        for i in range(len(labels)):

            if left_values[i] > right_values[i]:

                ax.barh(
                    y[i],
                    -left_values[i],
                    height=0.58,
                    facecolor="none",
                    edgecolor="white",
                    linewidth=2.2,
                )

            elif right_values[i] > left_values[i]:

                ax.barh(
                    y[i],
                    right_values[i],
                    height=0.58,
                    facecolor="none",
                    edgecolor="white",
                    linewidth=2.2,
                )

        ax.set_xlim(-110, 110)

        ax.set_xticks([])
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_title(
            "Fight Attribute Comparison",
            color="white",
            fontsize=15,
            fontweight="bold",
            pad=15,
        )

        plt.tight_layout()

        return fig
    
    def create_momentum_chart(
        self,
        fighter_one_name,
        fighter_two_name,
        fighter_one_values,
        fighter_two_values,
        title,
    ):

        import matplotlib.pyplot as plt

        rounds = [1, 2, 3, 4, 5]

        fig, ax = plt.subplots(figsize=(7.5, 3.8))

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        ax.plot(
            rounds,
            fighter_one_values,
            color="#00B4FF",
            linewidth=3,
            marker="o",
            markersize=7,
            label=fighter_one_name,
        )

        ax.plot(
            rounds,
            fighter_two_values,
            color="#FF4040",
            linewidth=3,
            marker="o",
            markersize=7,
            label=fighter_two_name,
        )

        ax.fill_between(rounds, fighter_one_values, alpha=0.15, color="#00B4FF")
        ax.fill_between(rounds, fighter_two_values, alpha=0.15, color="#FF4040")

        ax.set_xlim(1, 5)
        ax.set_ylim(0, 100)

        ax.set_xticks(rounds)
        ax.set_xticklabels(
            [f"R{i}" for i in rounds],
            color="white",
            fontsize=10,
        )

        ax.tick_params(axis="y", colors="white")

        ax.grid(color="#333333", linestyle="--", alpha=0.35)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_title(
            title,
            color="white",
            fontsize=13,
            fontweight="bold",
        )

        legend = ax.legend(frameon=False)

        for text in legend.get_texts():
            text.set_color("white")

        plt.tight_layout()

        return fig
        
    def create_advantage_chart(
        self,
        fighter_one_name,
        fighter_two_name,
        labels,
        fighter_one_values,
        fighter_two_values,
    ):
        import numpy as np
        import matplotlib.pyplot as plt

        labels = labels[::-1]
        fighter_one_values = fighter_one_values[::-1]
        fighter_two_values = fighter_two_values[::-1]

        y = np.arange(len(labels))
        height = 0.35

        fig, ax = plt.subplots(figsize=(8.5, 5.5))

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        ax.barh(
            y + height / 2,
            fighter_one_values,
            height,
            color="#00B4FF",
            label=fighter_one_name,
        )

        ax.barh(
            y - height / 2,
            fighter_two_values,
            height,
            color="#FF4040",
            label=fighter_two_name,
        )

        ax.set_yticks(y)
        ax.set_yticklabels(labels, color="white", fontsize=11)

        ax.set_xticks([])
        ax.set_xlabel("")

        ax.grid(axis="x", color="#333333", alpha=0.4)

        for spine in ax.spines.values():
            spine.set_visible(False)

        legend = ax.legend(frameon=False)

        for text in legend.get_texts():
            text.set_color("white")

        plt.tight_layout()

        return fig