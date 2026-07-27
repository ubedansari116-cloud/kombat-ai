class AICoach:

    def __init__(self):
        pass

    def analyse_fighter(
        self,
        fighter_name,
        stats,
    ):

        report = {}

        report["fight_iq"] = (
            stats["strike_defense"] * 0.35
            + stats["takedown_defense"] * 0.35
            + stats["striking_accuracy"] * 0.15
            + stats["takedown_accuracy"] * 0.15
        )

        report["experience"] = (
            stats["wins"] + stats["losses"]
        )

        report["physical"] = (
            (
                stats["height"] / 200
            ) * 40
            +
            (
                stats["reach"] / 200
            ) * 60
        )

        report["striking"] = (
            stats["striking_accuracy"] * 0.6
            + stats["splm"] * 10
            - stats["sapm"] * 5
        )

        report["wrestling"] = (
            stats["takedown_accuracy"]
            + stats["takedown_avg"] * 15
        )

        report["defence"] = (
            stats["strike_defense"] * 0.5
            + stats["takedown_defense"] * 0.5
        )

        report["strengths"] = self.detect_strengths(report)
        report["weaknesses"] = self.detect_weaknesses(report)

        style, description = self.identify_style(report)

        report["style"] = style
        report["style_description"] = description

        return report
    
    def detect_strengths(
        self,
        assessment,
    ):

        strengths = []

        if assessment["fight_iq"] >= 85:
            strengths.append("Elite Fight IQ")

        elif assessment["fight_iq"] >= 75:
            strengths.append("High Fight IQ")

        if assessment["striking"] >= 85:
            strengths.append("Elite Striking")

        elif assessment["striking"] >= 75:
            strengths.append("High-Level Striking")

        if assessment["wrestling"] >= 85:
            strengths.append("Elite Wrestling")

        elif assessment["wrestling"] >= 75:
            strengths.append("Strong Wrestling")

        if assessment["defence"] >= 85:
            strengths.append("Elite Defence")

        elif assessment["defence"] >= 75:
            strengths.append("Strong Defence")

        if assessment["physical"] >= 85:
            strengths.append("Elite Physical Tools")

        elif assessment["physical"] >= 75:
            strengths.append("Excellent Physical Tools")

        if len(strengths) == 0:
            strengths.append("Well Rounded Skill Set")

        return strengths
    
    def detect_weaknesses(
        self,
        assessment,
    ):

        weaknesses = []

        if assessment["fight_iq"] < 60:
            weaknesses.append("Decision Making")

        if assessment["striking"] < 60:
            weaknesses.append("Striking")

        if assessment["wrestling"] < 60:
            weaknesses.append("Wrestling")

        if assessment["defence"] < 60:
            weaknesses.append("Defence")

        if assessment["physical"] < 60:
            weaknesses.append("Physical Tools")

        if len(weaknesses) == 0:
            weaknesses.append("No Major Weaknesses Identified")

        return weaknesses
    
    def identify_style(
        self,
        assessment,
    ):

        striking = assessment["striking"]
        wrestling = assessment["wrestling"]
        defence = assessment["defence"]
        iq = assessment["fight_iq"]

        # Complete fighter
        if (
            striking >= 65
            and wrestling >= 65
            and defence >= 70
            and iq >= 70
        ):
            return (
                "Complete Mixed Martial Artist",
                "Highly effective across striking, wrestling and defence with very few exploitable weaknesses."
            )

        # Wrestling specialist
        if wrestling == max(striking, wrestling, defence):
            return (
                "Pressure Grappling Specialist",
                "Uses relentless wrestling pressure and positional control to dominate opponents."
            )

        # Striker
        if striking == max(striking, wrestling, defence):
            return (
                "Elite Striker",
                "Prefers to dictate fights through striking accuracy, timing and offensive pressure."
            )

        # Defensive technician
        if defence == max(striking, wrestling, defence):
            return (
                "Defensive Technician",
                "Wins through intelligent defence, patience and efficient counter fighting."
            )

        return (
            "Well Rounded Competitor",
            "Possesses a balanced skill set across multiple areas."
        )
        
