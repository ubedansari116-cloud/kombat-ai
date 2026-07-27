class RecommendationEngine:

    def __init__(self):
        self.style_database = {

        "Elite Wrestler": {

            "principles": [
                "Pressure",
                "Chain Wrestling",
                "Top Control",
                "Relentless Pace",
            ],

            "technical": [
                "Single Leg Entries",
                "Double Leg Entries",
                "Fence Wrestling",
                "Chain Wrestling",
                "Top Control",
            ],

            "conditioning": [
                "Anaerobic Conditioning",
                "Grip Strength",
                "Explosive Shots",
            ],

            "film": [
                "Study cage pressure",
                "Watch elite wrestling exchanges",
            ],

        },

        "Elite Striker": {

            "principles": [
                "Precision",
                "Distance Management",
                "Patience",
                "Counter Striking",
            ],

            "technical": [
                "Jab",
                "Footwork",
                "Head Movement",
                "Counter Punching",
                "Kickboxing Combinations",
            ],

            "conditioning": [
                "Reaction Speed",
                "Footwork Conditioning",
                "Explosive Power",
            ],

            "film": [
                "Study striking exchanges",
                "Watch counter opportunities",
            ],

        },

        "Tactical Veteran": {

            "principles": [
                "Fight IQ",
                "Adaptability",
                "Game Planning",
                "Discipline",
            ],

            "technical": [
                "Feints",
                "Distance Control",
                "Defensive Awareness",
                "Transition Game",
            ],

            "conditioning": [
                "Recovery",
                "Mobility",
                "Efficiency",
            ],

            "film": [
                "Study decision making",
                "Study tactical adjustments",
            ],

        },

        "Well Rounded Competitor": {

            "principles": [
                "Balanced Development",
                "Consistency",
                "Adaptability",
                "Fundamentals",
            ],

            "technical": [
                "Basic Striking",
                "Basic Wrestling",
                "Defence",
                "Transitions",
            ],

            "conditioning": [
                "General Conditioning",
                "Strength",
                "Mobility",
            ],

            "film": [
                "Study complete fighters",
            ],

        }

    }

    def build_training_blueprint(
        self,
        fighter_profile,
        user_goal,
        experience,
        training_days,
        fight_camp,
        weakness,
        training_environment,
    ):

        blueprint = {}

        # -------------------------
        # Primary Focus
        # -------------------------

        goal_map = {

            "Become a Better Striker":
                "Striking",

            "Become a Better Wrestler":
                "Wrestling",

            "Become More Well Rounded":
                "Balanced",

            "Prepare for Amateur MMA":
                "Balanced",

            "Prepare for Professional MMA":
                "Balanced",

            "Improve Cardio":
                "Conditioning",

        }

        blueprint["primary_focus"] = goal_map[user_goal]

        # -------------------------
        # Secondary Focus
        # -------------------------

        blueprint["secondary_focus"] = weakness

        # -------------------------
        # Training Volume
        # -------------------------

        if training_days <= 2:

            blueprint["training_volume"] = "Low"

        elif training_days <= 4:

            blueprint["training_volume"] = "Medium"

        else:

            blueprint["training_volume"] = "High"

        # -------------------------
        # Session Duration
        # -------------------------

        if experience == "Beginner":

            blueprint["session_duration"] = "60 minutes"

        elif experience == "Intermediate":

            blueprint["session_duration"] = "90 minutes"

        else:

            blueprint["session_duration"] = "120 minutes"

        # -------------------------
        # Intensity
        # -------------------------

        if fight_camp:

            blueprint["intensity"] = "Competition"

        elif experience == "Beginner":

            blueprint["intensity"] = "Controlled"

        else:

            blueprint["intensity"] = "Progressive"

        # -------------------------
        # Fighter Knowledge
        # -------------------------

        style = fighter_profile["style"]

        style_info = self.style_database.get(
            style,
            self.style_database["Well Rounded Competitor"],
        )

        blueprint["fighter_principles"] = style_info["principles"]

        blueprint["technical_focus"] = style_info["technical"]

        blueprint["conditioning_focus"] = style_info["conditioning"]

        blueprint["film_study"] = style_info["film"]

        # -------------------------
        # Training Priority Order
        # -------------------------

        priorities = []

        priorities.append(
            blueprint["primary_focus"]
        )

        if weakness not in priorities:

            priorities.append(weakness)

        if blueprint["primary_focus"] != "Conditioning":

            priorities.append("Conditioning")

        if "Fight IQ" not in priorities:

            priorities.append("Fight IQ")

        blueprint["priority_order"] = priorities

        # -------------------------
        # Environment
        # -------------------------

        blueprint["training_environment"] = training_environment

        blueprint["experience"] = experience

        blueprint["training_days"] = training_days

        blueprint["fight_camp"] = fight_camp

        return blueprint