import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow Streamlit to import files from the src folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from rag_advisor import KombatAdvisor
from radar import RadarChart

st.set_page_config(
    page_title="Kombat AI",
    page_icon="🥰",
    layout="wide",
)


@st.cache_resource
def load_advisor():
    return KombatAdvisor()


advisor = load_advisor()
radar = RadarChart()

st.title("🥰 Kombat AI")
st.divider()
st.markdown(
    """
### AI-Powered UFC Analytics Platform

Analyze fighters using:

- 🧠 Machine Learning Fight Prediction
- 📊 Tactical Attribute Radar
- ⚔ Statistical Matchup Analysis
- 📈 AI Fight Intelligence
"""
)

fighter_names = sorted(advisor.retriever.fighter_names)

left_column, right_column = st.columns(2)

with left_column:
    fighter_one = st.selectbox(
        "Fighter One",
        fighter_names,
        index=0,
    )

with right_column:
    default_second_index = 1 if len(fighter_names) > 1 else 0

    fighter_two = st.selectbox(
        "Fighter Two",
        fighter_names,
        index=default_second_index,
    )

compare_button = st.button(
    "Compare Fighters",
    type="primary",
    use_container_width=True,
)

if compare_button:

    if fighter_one == fighter_two:
        st.warning("Please select two different fighters.")

    else:

        with st.spinner("Analysing matchup..."):
            query = f"Compare {fighter_one} and {fighter_two}"
            result = advisor.answer(query)
            st.write(result.keys())

        prediction = result["prediction"]
        comparison = result["comparison"]
        summary = result["summary"]

        fighter_one_probability = prediction["fighter_one_probability"]
        fighter_two_probability = prediction["fighter_two_probability"]
        predicted_winner = prediction["predicted_winner"]

        # ===========================
        # TOP SECTION
        # ===========================

    left, right = st.columns([1, 1.35])

    with left:

        st.subheader("Fight Prediction")

        st.metric(
            "Predicted Winner",
            predicted_winner,
    )
        st.write("")
        st.write(f"**{fighter_one}**")
        st.progress(fighter_one_probability / 100)
        st.caption(f"{fighter_one_probability:.2f}%")
        
        st.write("")
        st.write(f"**{fighter_two}**")
        st.progress(fighter_two_probability / 100)
        st.caption(f"{fighter_two_probability:.2f}%")

        st.write("")

        st.subheader("Overall Statistical Edge")

        st.success(comparison["overall_edge"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                fighter_one,
                comparison["fighter_one_wins"],
        )

        with c2:
            st.metric(
                "Ties",
                comparison["ties"],
        )

        with c3:
            st.metric(
                fighter_two,
                comparison["fighter_two_wins"],
        )

    with right:

        st.subheader("Fighter Attribute Radar")

        figure = radar.create_chart(
            fighter_one_name=fighter_one,
            fighter_one_stats=result["fighters"][0]["stats"],
            fighter_two_name=fighter_two,
            fighter_two_stats=result["fighters"][1]["stats"],
            )

        st.pyplot(
            figure,
            clear_figure=True,
            )
        st.divider()

        # ===========================
        # FIGHT IQ ANALYSIS
        # ===========================

    st.subheader("🧠 Fight IQ Analysis")

    f1 = result["fight_iq"]["fighter_one"]
    f2 = result["fight_iq"]["fighter_two"]

    left, right = st.columns(2)

    with left:

        st.markdown(f"## {fighter_one}")
        st.metric("Fight IQ", f1["fight_iq"])
        st.success(f1["grade"])

        st.markdown("### 💪 Strengths")
        if f1["strengths"]:
            for strength in f1["strengths"]:
                st.write(f"✅ {strength}")
        else:
            st.write("No standout strengths detected.")

        st.markdown("### ⚠ Weaknesses")
        if f1["weaknesses"]:
            for weakness in f1["weaknesses"]:
                st.write(f"⚠ {weakness}")
        else:
            st.write("No major weaknesses detected.")

        st.markdown("### 🎯 Gameplan")
        for tip in f1["gameplan"]:
            st.write(f"• {tip}")

    with right:

        st.markdown(f"## {fighter_two}")
        st.metric("Fight IQ", f2["fight_iq"])
        st.success(f2["grade"])

        st.markdown("### 💪 Strengths")
        if f2["strengths"]:
            for strength in f2["strengths"]:
                st.write(f"✅ {strength}")
        else:
            st.write("No standout strengths detected.")

        st.markdown("### ⚠ Weaknesses")
        if f2["weaknesses"]:
            for weakness in f2["weaknesses"]:
                st.write(f"⚠ {weakness}")
        else:
            st.write("No major weaknesses detected.")

        st.markdown("### 🎯 Gameplan")
        for tip in f2["gameplan"]:
            st.write(f"• {tip}")

        # ===========================
        # SUMMARY
        # ===========================

    st.subheader("Analyst Summary")
    st.info(summary)

    st.divider()

        # ===========================
        # COMPARISON TABLE
        # ===========================

    st.subheader("📊 Statistical Comparison")

    for item in comparison["advantages"]:

        winner = item["winner"]

        if winner == fighter_one:
            icon = "🟥"
        elif winner == fighter_two:
            icon = "🟦"
        else:
            icon = "⚪"

        left, middle, right = st.columns([4, 1, 4], vertical_alignment="center")

        with left:
            st.markdown(
            f"<div style='text-align:left;font-weight:bold'>{fighter_one}</div>",
            unsafe_allow_html=True,
        )
            st.markdown(
            f"<h2 style='text-align:left'>{item['fighter_one_value']}</h2>",
            unsafe_allow_html=True,
        )

        with middle:
            st.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-size:34px;">{icon}</div>
                <div style="font-size:14px;margin-top:8px;">
                    {item["metric"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with right:
            st.markdown(
            f"<div style='text-align:right;font-weight:bold'>{fighter_two}</div>",
            unsafe_allow_html=True,
        )
            st.markdown(
            f"<h2 style='text-align:right'>{item['fighter_two_value']}</h2>",
            unsafe_allow_html=True,
        )

        st.divider()