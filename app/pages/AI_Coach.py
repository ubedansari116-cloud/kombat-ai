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

st.title("🧠 AI Coach")

st.caption(
    "Performance analysis, coaching insights and personalised improvement plans."
)

st.divider()

st.columns(1)

with st.container():
    fighter_name = st.selectbox(
        "Select Fighter",
        fighter_names,
    )


st.divider()

generate_report = st.button(
    "Generate AI Report",
    type="primary",
    use_container_width=True,
)

if generate_report:

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