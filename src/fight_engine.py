from copy import deepcopy


class FightEngine:
    """
    Core tactical engine powering:
    - Fight IQ
    - Tactical analysis
    - What If simulator
    - Future style simulations
    """

    def __init__(self):
        self.attribute_weights = {
            "striking": 0.22,
            "defense": 0.18,
            "wrestling": 0.18,
            "grappling": 0.15,
            "physical": 0.12,
            "experience": 0.15,
        }

    # ---------------------------------------------------
    # Helpers
    # ---------------------------------------------------

    @staticmethod
    def clamp(value, minimum=0, maximum=100):
        return max(minimum, min(maximum, value))

    # ---------------------------------------------------
    # Attribute Builder
    # ---------------------------------------------------

    def calculate_attributes(self, stats):
        """
        Converts raw UFC statistics into normalized
        0-100 combat attributes.
        """

        striking = (
            stats["striking_accuracy"] * 0.55
            + stats["splm"] * 8
            - stats["sapm"] * 3
        )

        defense = (
            stats["strike_defense"] * 0.55 + stats["takedown_defense"] * 0.45
        )

        wrestling = (
            stats["takedown_avg"] * 18 + stats["takedown_accuracy"] * 0.60
        )

        grappling = stats["submission_avg"] * 35 + stats["takedown_avg"] * 8

        physical = (stats["reach"] / 200) * 60 + (stats["height"] / 200) * 40

        total_fights = stats["wins"] + stats["losses"]

        if total_fights == 0:
            experience = 50

        else:
            win_rate = stats["wins"] / total_fights

            experience = win_rate * 70 + min(total_fights, 40) / 40 * 30

        return {
            "striking": self.clamp(striking),
            "defense": self.clamp(defense),
            "wrestling": self.clamp(wrestling),
            "grappling": self.clamp(grappling),
            "physical": self.clamp(physical),
            "experience": self.clamp(experience),
        }

    # ---------------------------------------------------
    # Fight IQ Score
    # ---------------------------------------------------

    def calculate_fight_iq(self, attributes):

        score = 0

        for attribute, weight in self.attribute_weights.items():
            score += attributes[attribute] * weight

        return round(score, 1)
    
    def generate_report(self, stats):

        attributes = self.calculate_attributes(stats)
        score = self.calculate_fight_iq(attributes)

        if score >= 90:
            grade = "🟢 Elite"
        elif score >= 80:
            grade = "🔵 A"
        elif score >= 70:
            grade = "🟡 B"
        elif score >= 60:
            grade = "🟠 C"
        else:
            grade = "🔴 D"

        strengths = []
        weaknesses = []
        gameplan = []

        # ---------- Strengths ----------

        if attributes["striking"] >= 80:
            strengths.append("Elite striking")

        if attributes["wrestling"] >= 80:
            strengths.append("Elite wrestling")

        if attributes["grappling"] >= 80:
            strengths.append("Elite grappling")

        if attributes["defense"] >= 80:
            strengths.append("Excellent defensive awareness")

        if attributes["physical"] >= 85:
            strengths.append("Excellent physical tools")

        # ---------- Weaknesses ----------

        if attributes["defense"] < 45:
            weaknesses.append("Can be hit consistently")

        if attributes["wrestling"] < 35:
            weaknesses.append("Vulnerable to takedowns")

        if stats["sapm"] > 6:
            weaknesses.append("Absorbs significant damage")

        if attributes["grappling"] < 35:
            weaknesses.append("Limited submission threat")

        # ---------- Gameplan ----------

        if attributes["striking"] > attributes["wrestling"]:
            gameplan.append("Keep the fight standing.")

        if attributes["wrestling"] > attributes["striking"]:
            gameplan.append("Mix in takedowns.")

        if attributes["physical"] > 80:
            gameplan.append("Use pace and pressure.")

        if attributes["grappling"] > 75:
            gameplan.append("Threaten submissions when opportunities arise.")

        if not gameplan:
            gameplan.append(
                "Maintain a balanced approach and adjust throughout the fight."
            )

        return {
            "fight_iq": score,
            "grade": grade,
            "attributes": attributes,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "gameplan": gameplan,
        }

    
    # ---------------------------------------------------
    # Compare Attributes
    # ---------------------------------------------------

    def compare_attributes(
        self,
        attributes_one,
        attributes_two,
    ):

        comparison = []

        for category in attributes_one:

            first = attributes_one[category]
            second = attributes_two[category]

            if abs(first - second) < 4:

                winner = "Even"

            elif first > second:

                winner = "fighter_one"

            else:

                winner = "fighter_two"

            comparison.append(
                {
                    "category": category.title(),
                    "fighter_one": round(first, 1),
                    "fighter_two": round(second, 1),
                    "winner": winner,
                }
            )

        return comparison

        # ---------------------------------------------------

    # What If Simulation
    # ---------------------------------------------------

    def simulate_changes(
        self,
        fighter_one_stats,
        fighter_two_stats,
        changes=None,
    ):

        fighter_one = deepcopy(fighter_one_stats)
        fighter_two = deepcopy(fighter_two_stats)

        if changes:

            if "fighter_one" in changes:
                fighter_one.update(changes["fighter_one"])

            if "fighter_two" in changes:
                fighter_two.update(changes["fighter_two"])

        return self.analyze(
            fighter_one,
            fighter_two,
        )

    # ---------------------------------------------------
    # Main Analysis Engine
    # ---------------------------------------------------

    def analyze(
        self,
        fighter_one_stats,
        fighter_two_stats,
    ):

        fighter_one_attributes = self.calculate_attributes(fighter_one_stats)

        fighter_two_attributes = self.calculate_attributes(fighter_two_stats)

        fighter_one_score = self.calculate_fight_iq(
            fighter_one_attributes
        ) + self.calculate_style_bonus(fighter_one_attributes)

        fighter_two_score = self.calculate_fight_iq(
            fighter_two_attributes
        ) + self.calculate_style_bonus(fighter_two_attributes)

        fighter_one_score = round(fighter_one_score, 1)
        fighter_two_score = round(fighter_two_score, 1)

        fighter_one_strengths = self.generate_strengths(fighter_one_stats)

        fighter_two_strengths = self.generate_strengths(fighter_two_stats)

        fighter_one_weaknesses = self.generate_weaknesses(fighter_one_stats)

        fighter_two_weaknesses = self.generate_weaknesses(fighter_two_stats)

        fighter_one_plan = self.generate_gameplan(
            "fighter_one",
            fighter_one_stats,
            "fighter_two",
            fighter_two_stats,
        )

        fighter_two_plan = self.generate_gameplan(
            "fighter_two",
            fighter_two_stats,
            "fighter_one",
            fighter_one_stats,
        )

        comparison = self.compare_attributes(
            fighter_one_attributes,
            fighter_two_attributes,
        )

        if fighter_one_score > fighter_two_score:

            overall_edge = "fighter_one"

        elif fighter_two_score > fighter_one_score:

            overall_edge = "fighter_two"

        else:

            overall_edge = "Even"

        return {
            "fighter_one": {
                "fight_iq": fighter_one_score,
                "attributes": fighter_one_attributes,
                "strengths": fighter_one_strengths,
                "weaknesses": fighter_one_weaknesses,
                "gameplan": fighter_one_plan,
            },
            "fighter_two": {
                "fight_iq": fighter_two_score,
                "attributes": fighter_two_attributes,
                "strengths": fighter_two_strengths,
                "weaknesses": fighter_two_weaknesses,
                "gameplan": fighter_two_plan,
            },
            "comparison": comparison,
            "overall_edge": overall_edge,
        }
