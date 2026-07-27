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
        
    def _rank_technical_focus(
        self,
        technical,
        experience,
        fight_camp,
        primary_focus,
        weakness,
        training_days,
    ):

        ranked = technical.copy()

        if primary_focus == "Wrestling":

            if experience == "Beginner":

                priority = [
                    "Single Leg Entries",
                    "Double Leg Entries",
                    "Top Control",
                    "Chain Wrestling",
                    "Fence Wrestling",
                ]

            else:

                priority = [
                    "Chain Wrestling",
                    "Fence Wrestling",
                    "Top Control",
                    "Double Leg Entries",
                    "Single Leg Entries",
                ]

        elif primary_focus == "Striking":

            if experience == "Beginner":

                priority = [
                    "Jab",
                    "Footwork",
                    "Head Movement",
                    "Counter Punching",
                    "Kickboxing Combinations",
                ]

            else:

                priority = [
                    "Counter Punching",
                    "Kickboxing Combinations",
                    "Head Movement",
                    "Footwork",
                    "Jab",
                ]

        else:

            return ranked

        ordered = []

        for item in priority:

            if item in ranked:

                ordered.append(item)

        for item in ranked:

            if item not in ordered:

                ordered.append(item)
        
        if fight_camp:

            if "Chain Wrestling" in ordered:

                ordered.remove("Chain Wrestling")
                ordered.insert(0, "Chain Wrestling")

            if "Counter Punching" in ordered:

                ordered.remove("Counter Punching")
                ordered.insert(0, "Counter Punching")

        if weakness == "Wrestling":

            for skill in [
                "Single Leg Entries",
                "Double Leg Entries",
                "Chain Wrestling",
            ]:

                if skill in ordered:

                    ordered.remove(skill)
                    ordered.insert(0, skill)

        if training_days <= 2:

            simplified = []

            for skill in ordered:

                if skill not in [
                    "Fence Wrestling",
                    "Chain Wrestling",
                ]:

                    simplified.append(skill)

            ordered = simplified

        return ordered
    
    def _rank_conditioning_focus(
        self,
        conditioning,
        primary_focus,
        fight_camp,
        weakness,
        training_environment,
    ):

        ordered = conditioning.copy()

        if primary_focus == "Conditioning":

            priority = [
                "Anaerobic Conditioning",
                "Grip Strength",
                "Explosive Shots",
                "Reaction Speed",
                "Footwork Conditioning",
                "Explosive Power",
                "General Conditioning",
                "Strength",
                "Mobility",
            ]

        elif primary_focus == "Wrestling":

            priority = [
                "Grip Strength",
                "Anaerobic Conditioning",
                "Explosive Shots",
                "Strength",
                "Mobility",
            ]

        elif primary_focus == "Striking":

            priority = [
                "Reaction Speed",
                "Footwork Conditioning",
                "Explosive Power",
                "Mobility",
                "General Conditioning",
            ]

        else:

            priority = ordered

        ranked = []

        for item in priority:

            if item in ordered:

                ranked.append(item)

        for item in ordered:

            if item not in ranked:

                ranked.append(item)

        if weakness == "Cardio":

            if "Anaerobic Conditioning" in ranked:

                ranked.remove("Anaerobic Conditioning")
                ranked.insert(0, "Anaerobic Conditioning")

            if "General Conditioning" in ranked:

                ranked.remove("General Conditioning")
                ranked.insert(1, "General Conditioning")

        if fight_camp:

            if "Explosive Power" in ranked:

                ranked.remove("Explosive Power")
                ranked.insert(0, "Explosive Power")

        if training_environment == "Home Gym":

            if "Mobility" in ranked:

                ranked.remove("Mobility")
                ranked.insert(0, "Mobility")

            if "General Conditioning" in ranked:

                ranked.remove("General Conditioning")
                ranked.insert(1, "General Conditioning")

        elif training_environment == "Professional Gym":

            if "Grip Strength" in ranked:

                ranked.remove("Grip Strength")
                ranked.insert(0, "Grip Strength")

            if "Explosive Power" in ranked:

                ranked.remove("Explosive Power")
                ranked.insert(1, "Explosive Power")
        return ranked
    
    def _rank_film_study(
        self,
        film,
        primary_focus,
        fight_camp,
        experience,
    ):

        ordered = film.copy()

        if primary_focus == "Wrestling":

            priority = [
                "Study cage pressure",
                "Watch elite wrestling exchanges",
            ]

        elif primary_focus == "Striking":

            priority = [
                "Study striking exchanges",
                "Watch counter opportunities",
            ]

        elif primary_focus == "Balanced":

            priority = [
                "Study complete fighters",
                "Study decision making",
                "Study tactical adjustments",
            ]

        elif primary_focus == "Conditioning":

            priority = [
                "Study complete fighters",
                "Study cage pressure",
            ]

        else:

            priority = ordered

        ranked = []

        for item in priority:

            if item in ordered:

                ranked.append(item)

        for item in ordered:

            if item not in ranked:

                ranked.append(item)

        if fight_camp:

            if "Study tactical adjustments" in ranked:

                ranked.remove("Study tactical adjustments")
                ranked.insert(0, "Study tactical adjustments")

        if experience == "Beginner":

            if "Study complete fighters" in ranked:

                ranked.remove("Study complete fighters")
                ranked.insert(0, "Study complete fighters")

        return ranked

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

        blueprint["technical_focus"] = self._rank_technical_focus(
            style_info["technical"],
            experience,
            fight_camp,
            blueprint["primary_focus"],
            weakness,
            training_days,
        )

        blueprint["conditioning_focus"] = self._rank_conditioning_focus(
            style_info["conditioning"],
            blueprint["primary_focus"],
            fight_camp,
            weakness,
            training_environment,
        )

        blueprint["film_study"] = self._rank_film_study(
            style_info["film"],
            blueprint["primary_focus"],
            fight_camp,
            experience,
        )

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