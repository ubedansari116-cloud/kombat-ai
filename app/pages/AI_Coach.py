import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from src.rag_advisor import KombatAdvisor
from src.fighter_repository import FighterRepository
from src.ai_coach import AICoach
from src.recommendation_engine import RecommendationEngine
from src.memory_engine import MemoryEngine
from src.llm_coach import LLMCoach

st.set_page_config(
    page_title="AI Coach",
    page_icon="🧠",
    layout="wide",
)

@st.cache_resource
def load_advisor():
    return KombatAdvisor()

repository = FighterRepository()
fighter_names = repository.get_all_fighters()
advisor = load_advisor()
ai_coach = AICoach()
recommendation_engine = RecommendationEngine()
coach = LLMCoach()
memory = MemoryEngine()
saved_profile = memory.recall_user("general")

st.title("🧠 AI Coach")

st.caption(
    "Your chosen fighter serves as a blueprint, not a destination. " \
    "Kombat AI combines their fighting principles with your goals, " \
    "experience and training profile to generate coaching tailored specifically to you."
)

st.divider()

st.columns(1)

with st.container():
    fighter_name = st.selectbox(
        "Select Fighter",
        fighter_names,
    )


st.divider()

if st.button(
    "Generate AI Report",
    type="primary",
    use_container_width=True,
):
    st.session_state["report_generated"] = True
    st.session_state["training_plan"] = False

if st.session_state.get("report_generated", False):

    profile = repository.get_fighter(fighter_name)

    stats = profile["stats"].copy()
    
    assessment = advisor.ai_coach.analyse_fighter(
        fighter_name,
        stats,
    )

    st.header(f"🥊 {fighter_name}")

    st.divider()

    # ----------------------------
    # Derived Metrics
    # ----------------------------

    total_fights = stats["wins"] + stats["losses"]

    fight_iq = (
        stats["strike_defense"] * 0.35
        + stats["takedown_defense"] * 0.35
        + stats["striking_accuracy"] * 0.15
        + stats["takedown_accuracy"] * 0.15
    )

    fight_iq = round(fight_iq, 1)

    col1, col2, col3 = st.columns(3)

    # ==========================
    # Record
    # ==========================

    with col1:

        st.metric(
            "Record",
            f"{stats['wins']} - {stats['losses']}",
        )

        st.metric(
            "KO Wins",
            stats.get("ko_wins", "N/A"),
        )

        st.metric(
            "Submission Wins",
            stats.get("submission_wins", "N/A"),
        )

    # ==========================
    # Athlete
    # ==========================

    with col2:

        st.metric(
            "height/reach",
            f"{stats['height']}cm/{stats['reach']}cm",
        )

        st.metric(
            "Experience",
            f"{total_fights} fights",
        )

        st.metric(
            "Fight IQ",
            f"{assessment['fight_iq']:.1f}/100",
        )

    # ==========================
    # Performance
    # ==========================

    with col3:

        st.metric(
            "Striking",
            f"{assessment['striking']:.1f}/100",
        )

        st.metric(
            "Wrestling",
            f"{assessment['wrestling']:.1f}/100",
        )

        st.metric(
            "Defence",
            f"{assessment['defence']:.1f}/100",
        )

    st.divider()

    st.subheader("🥋 Fighter Identity")

    st.markdown(f"### {assessment['style']}")

    st.write(assessment["style_description"])

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("⭐ Elite Strengths")

        for strength in assessment["strengths"]:

            st.success(strength)

    with right:

        st.subheader("⚠ Areas to Improve")

        for weakness in assessment["weaknesses"]:

            st.warning(weakness)

    st.divider()

    st.subheader("🏋 Athlete Profile")

    left, right = st.columns(2)

    with left:

        user_goal = st.selectbox(
            "Primary Goal",
            [
                "Become a Better Striker",
                "Become a Better Wrestler",
                "Become More Well Rounded",
                "Prepare for Amateur MMA",
                "Prepare for Professional MMA",
                "Improve Cardio",
            ],
        )

        user_level = st.selectbox(
            "Experience Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )

        training_days = st.slider(
            "Training Days Per Week",
            1,
            7,
            4,
        )

    with right:

        preparing_for_fight = st.toggle(
            "Currently Preparing For A Fight",
        )

        user_weakness = st.selectbox(
            "Your Biggest Weakness",
            [
                "Striking",
                "Wrestling",
                "Defence",
                "Cardio",
                "Fight IQ",
            ],
        )

        training_environment = st.selectbox(
            "Training Environment",
            [
                "Home Training",
                "Local Gym",
                "Professional MMA Gym",
            ],
        )

    st.divider()

    if st.button(
        "🧠 Generate Personal Training Plan",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["training_plan"] = True

if st.session_state.get("training_plan", False):
    blueprint = recommendation_engine.build_training_blueprint(
        fighter_profile=assessment,
        user_goal=user_goal,
        experience=user_level,
        training_days=training_days,
        fight_camp=preparing_for_fight,
        weakness=user_weakness,
        training_environment=training_environment,
    )

    training_report = coach.generate_training_plan(
        athlete_profile=saved_profile,
        blueprint=blueprint,
        memory=saved_profile,
    )

    st.divider()

    st.subheader("🤖 AI Coach")

    st.markdown(training_report)

    # --------------------------
    # Save User Memory
    # --------------------------

    memory.remember_user(

        "general",

        {

            "fighter": fighter_name,
            "goal": user_goal,
            "experience": user_level,
            "training_days": training_days,
            "fight_camp": preparing_for_fight,
            "weakness": user_weakness,
            "training_environment": training_environment,

        }

    )

    st.divider()

    st.subheader("🎯 Personal Training Blueprint")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Primary Focus",
            blueprint["primary_focus"],
        )

        st.metric(
            "Secondary Focus",
            blueprint["secondary_focus"],
        )

        st.metric(
            "Training Volume",
            blueprint["training_volume"],
        )

        st.metric(
            "Session Duration",
            blueprint["session_duration"],
        )

    with right:

        st.metric(
            "Intensity",
            blueprint["intensity"],
        )

        st.write("### Fighter Principles")

        for principle in blueprint["fighter_principles"]:

            st.success(principle)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🥋 Technical Focus")

        for drill in blueprint["technical_focus"]:

            st.info(drill)

    with col2:

        st.subheader("🏃 Conditioning Focus")

        for item in blueprint["conditioning_focus"]:

            st.warning(item)

    st.divider()

    st.subheader("🎥 Film Study")

    for video in blueprint["film_study"]:

        st.success(video)

    st.divider()

    st.write("### Training Priority")

    for index, priority in enumerate(
        blueprint["priority_order"],
        start=1,
    ):

        st.info(
            f"{index}. {priority}"
        )