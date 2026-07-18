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

    # ---------------------------------------------------
    # Fight IQ Grade
    # ---------------------------------------------------

    def fight_iq_grade(self, score):

        if score >= 95:
            return "🟣 S+"

        elif score >= 90:
            return "🔵 S"

        elif score >= 85:
            return "🟢 A"

        elif score >= 80:
            return "🟡 B"

        elif score >= 70:
            return "🟠 C"

        return "🔴 D"
    
    # ---------------------------------------------------
    # Style Bonus
    # ---------------------------------------------------

    def calculate_style_bonus(self, attributes):

        bonus = 0

        if attributes["wrestling"] > 80:
            bonus += 3

        if attributes["grappling"] > 80:
            bonus += 2

        if attributes["striking"] > 85:
            bonus += 2

        if attributes["defense"] > 85:
            bonus += 2

        if attributes["striking"] > 75 and attributes["defense"] > 75:
            bonus += 2

        if attributes["wrestling"] > 75 and attributes["grappling"] > 75:
            bonus += 2

        return bonus

    # ---------------------------------------------------
    # Strength Detection
    # ---------------------------------------------------

    def generate_strengths(self, stats):

        strengths = []

        if stats["striking_accuracy"] >= 55:
            strengths.append("Elite striking accuracy")

        if stats["splm"] >= 5:
            strengths.append("High striking output")

        if stats["strike_defense"] >= 60:
            strengths.append("Excellent striking defence")

        if stats["takedown_avg"] >= 2.5:
            strengths.append("Dangerous offensive wrestling")

        if stats["takedown_accuracy"] >= 50:
            strengths.append("Efficient takedowns")

        if stats["takedown_defense"] >= 80:
            strengths.append("Elite takedown defence")

        if stats["submission_avg"] >= 1:
            strengths.append("Submission threat")

        if stats["wins"] >= 20:
            strengths.append("Highly experienced")

        return strengths

        # ---------------------------------------------------

    # Weakness Detection
    # ---------------------------------------------------

    def generate_weaknesses(self, stats):

        weaknesses = []

        if stats["striking_accuracy"] < 40:
            weaknesses.append("Low striking accuracy")

        if stats["sapm"] > 4:
            weaknesses.append("Absorbs significant damage")

        if stats["strike_defense"] < 50:
            weaknesses.append("Can be hit consistently")

        if stats["takedown_avg"] < 1:
            weaknesses.append("Limited offensive wrestling")

        if stats["takedown_accuracy"] < 35:
            weaknesses.append("Low takedown success")

        if stats["takedown_defense"] < 60:
            weaknesses.append("Vulnerable to takedowns")

        if stats["submission_avg"] < 0.2:
            weaknesses.append("Limited submission threat")

        return weaknesses

    # ---------------------------------------------------
    # Tactical Gameplan
    # ---------------------------------------------------

    def generate_gameplan(
        self,
        fighter_name,
        fighter_stats,
        opponent_name,
        opponent_stats,
    ):

        plan = []

        # ---------- STRIKING ----------

        if (
            fighter_stats["striking_accuracy"]
            > opponent_stats["striking_accuracy"]
        ):
            plan.append("Use striking advantage to control exchanges.")

        # ---------- WRESTLING ----------

        if fighter_stats["takedown_avg"] > opponent_stats["takedown_avg"] + 1:
            plan.append("Mix wrestling early to dictate the pace.")

        # ---------- SUBMISSIONS ----------

        if opponent_stats["submission_avg"] >= 1:
            plan.append("Avoid extended grappling exchanges.")

        # ---------- DEFENSE ----------

        if fighter_stats["strike_defense"] < opponent_stats["strike_defense"]:
            plan.append(
                "Maintain head movement and avoid prolonged exchanges."
            )

        # ---------- RANGE ----------

        if fighter_stats["reach"] > opponent_stats["reach"] + 5:
            plan.append("Fight behind the jab and maintain range.")

        # ---------- PRESSURE ----------

        if fighter_stats["sapm"] < opponent_stats["sapm"]:
            plan.append("Pressure the opponent and force mistakes.")

        if len(plan) == 0:

            plan.append(
                "Maintain a balanced approach and adjust throughout the fight."
            )

        return plan

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
    
    def matchup_insight(
            self,
            fighter_one_name,
            fighter_one_stats,
            fighter_two_name,
            fighter_two_stats,
            ):
        insights = []
        
        if (
            fighter_one_stats["takedown_avg"] > 2.5
            and fighter_two_stats["submission_avg"] > 1
            ):
            insights.append(
                f"{fighter_one_name}'s wrestling could neutralize "
                f"{fighter_two_name}'s submission game."
                )

        if (
            fighter_two_stats["takedown_avg"] > 2.5
            and fighter_one_stats["submission_avg"] > 1
            ):
            insights.append(
                f"{fighter_two_name}'s wrestling could neutralize "
                f"{fighter_one_name}'s submission game."
                )

        if (
            fighter_one_stats["reach"]
            >
            fighter_two_stats["reach"] + 8
            ):
            insights.append(
                f"{fighter_one_name} should fight behind the jab and maintain range."
                )

        if (
            fighter_two_stats["reach"]
            >
            fighter_one_stats["reach"] + 8
            ):
            insights.append(
                f"{fighter_two_name} should fight behind the jab and maintain range."
                )

        if (
            fighter_one_stats["strike_defense"]
            <
            fighter_two_stats["strike_defense"]
            ):
            insights.append(
                f"{fighter_one_name} cannot afford prolonged striking exchanges."
                )

        if (
            fighter_two_stats["strike_defense"]
            <
            fighter_one_stats["strike_defense"]
            ):
            insights.append(
                f"{fighter_two_name} cannot afford prolonged striking exchanges."
                )
            return insights

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
    fighter_one_name,
    fighter_one_stats,
    fighter_two_name,
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

        fighter_one_grade = self.fight_iq_grade(
            fighter_one_score
            )
        fighter_two_grade = self.fight_iq_grade(
            fighter_two_score
            )

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

            overall_edge = fighter_one_name

        elif fighter_two_score > fighter_one_score:

            overall_edge = fighter_two_name

        else:

            overall_edge = "Even"
            
        matchup = self.matchup_insight(
            fighter_one_name,
            fighter_one_stats,
            fighter_two_name,
            fighter_two_stats,
            )
        
        return {
            "matchup_analysis": matchup,
            "fighter_one": {
                "name": fighter_one_name,
                "fight_iq": fighter_one_score,
                "grade": fighter_one_grade,
                "attributes": fighter_one_attributes,
                "strengths": fighter_one_strengths,
                "weaknesses": fighter_one_weaknesses,
                "gameplan": fighter_one_plan,
            },
            "fighter_two": {
                "name": fighter_two_name,
                "fight_iq": fighter_two_score,
                "grade": fighter_two_grade,
                "attributes": fighter_two_attributes,
                "strengths": fighter_two_strengths,
                "weaknesses": fighter_two_weaknesses,
                "gameplan": fighter_two_plan,
            },
            "comparison": comparison,
            "overall_edge": overall_edge,
        }
