import numpy as np
import matplotlib.pyplot as plt


class RadarChart:
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

        values = [
            self.clamp(striking),
            self.clamp(defense),
            self.clamp(wrestling),
            self.clamp(grappling),
            self.clamp(physical),
            self.clamp(experience),
        ]

        return values

    def create_chart(
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
            figsize=(4.6, 4.6),
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

        return fig