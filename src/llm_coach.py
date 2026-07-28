import os

from dotenv import load_dotenv
from google import genai
from src.prompts import SYSTEM_PROMPT
from src.prompts import WHATIF_PROMPT

load_dotenv()


class LLMCoach:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found inside .env"
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model = "models/gemini-3.5-flash"

    def generate_training_plan(
        self,
        athlete_profile,
        blueprint,
        memory,
    ):

        prompt = f"""
        {SYSTEM_PROMPT}

        =================================================
        MISSION
        =================================================

        You are preparing this athlete for real MMA competition.

        The recommendation engine has already analysed the athlete.

        DO NOT:

        - recalculate priorities
        - change the blueprint
        - invent weaknesses
        - contradict the supplied information

        Your only responsibility is to transform the blueprint into elite coaching.

        =================================================
        ATHLETE PROFILE
        =================================================

        {athlete_profile}

        =================================================
        TRAINING BLUEPRINT
        =================================================

        {blueprint}

        =================================================
        ATHLETE HISTORY
        =================================================

        {memory}

        =================================================
        RESPONSE REQUIREMENTS
        =================================================

        Your response must remain between 700 and 900 words.

        Write naturally.

        Avoid repeating yourself.

        Every recommendation must be personalised.

        Keep explanations short and practical.

        Never write like a textbook.

        Never mention you are an AI.

        Every recommendation should have a purpose.

        =================================================
        STRUCTURE
        =================================================

        # Weekly Objective

        2-3 sentences.

        -------------------------------------------------

        # Monday

        Technical Focus

        Conditioning

        Recovery

        Film Study

        Why it matters
        (ONE sentence.)

        -------------------------------------------------

        Repeat the exact same structure for

        Tuesday

        Wednesday

        Thursday

        Friday

        Saturday

        Sunday

        -------------------------------------------------

        # Coach's Notes

        Write 3-5 short paragraphs.

        Talk directly to the athlete.

        Be motivational.

        Be brutally honest when necessary.

        Sound like a UFC head coach before fight camp.

        End with ONE memorable sentence.

        =================================================
        STYLE
        =================================================

        Write like Trevor Wittman,
        Javier Mendez,
        or Eugene Bareman.

        Short.

        Confident.

        Specific.

        Professional.

        No fluff.
        """
        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if response.text:
                return response.text

            return "Unable to generate coaching report."

        except Exception as e:

            return f"AI Coach unavailable.\n\n{e}"
        
    def generate_fight_breakdown(
        self,
        fighter_a,
        fighter_b,
        simulation,
    ):
        prompt = f"""
        {WHATIF_PROMPT}

        ================================

        FIGHTER A

        {fighter_a}

        ================================

        FIGHTER B

        {fighter_b}

        ================================

        SIMULATION

        {simulation}

        ================================

        Create:

        # Prediction

        # Why

        # Keys to Victory

        ## Fighter A

        ...

        ## Fighter B

        ...

        # Biggest X-Factor

        # Final Verdict

        Limit to 600–800 words.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            return response.text

        except Exception:

            return None