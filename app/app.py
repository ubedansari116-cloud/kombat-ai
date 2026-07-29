import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow imports from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_advisor import KombatAdvisor
from src.radar import FightVisualizer

st.set_page_config(
    page_title="Kombat AI",
    page_icon="🥰",
    layout="wide",
)


@st.cache_resource
def load_advisor():
    return KombatAdvisor()


advisor = load_advisor()
visualizer = FightVisualizer()

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

        prediction = result["prediction"]
        comparison = result["comparison"]
        summary = result["summary"]
        f1 = result["fight_iq"]["fighter_one"]
        f2 = result["fight_iq"]["fighter_two"]

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

        figure = visualizer.create_radar_chart(
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

    left_graph, right_graph = st.columns(2)

    with left_graph:

        st.markdown("### 🥊 Stand-Up Momentum")

        standup_fig = visualizer.create_momentum_chart(
            fighter_one_name=fighter_one,
            fighter_two_name=fighter_two,
            fighter_one_values=f1["standup_curve"],
            fighter_two_values=f2["standup_curve"],
            title="Stand-Up Control Over 5 Rounds",
        )

        st.pyplot(standup_fig, clear_figure=True)

    with right_graph:

        st.markdown("### 🤼 Ground Control Momentum")

        ground_fig = visualizer.create_momentum_chart(
            fighter_one_name=fighter_one,
            fighter_two_name=fighter_two,
            fighter_one_values=f1["ground_curve"],
            fighter_two_values=f2["ground_curve"],
            title="Ground Control Over 5 Rounds",
        )

        st.pyplot(ground_fig, clear_figure=True)

    st.divider()

    st.subheader("📊 Fight IQ Comparison")

    comparison_chart = visualizer.create_attribute_comparison(
        fighter_one_name=fighter_one,
        fighter_two_name=fighter_two,
        fighter_one_stats=result["fighters"][0]["stats"],
        fighter_two_stats=result["fighters"][1]["stats"],
    )
    

    st.pyplot(comparison_chart, clear_figure=True)
 
    st.markdown("## 🎯 Tactical Breakdown")

    left_tactical, right_tactical = st.columns(2)

    with left_tactical:

        st.markdown(f"### {fighter_one}")

        st.markdown("### ⭐ Primary Weapons")

        for strength in f1["strengths"]:
            st.markdown(
                f"""
                <div style="
                    background:#173322;
                    color:white;
                    border-left:5px solid #22c55e;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {strength}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### 🚨 Vulnerabilities")

        for weakness in f1["weaknesses"]:
            st.markdown(
                f"""
                <div style="
                    background:#3a2b12;
                    color:white; 
                    border-left:5px solid #f59e0b;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {weakness}
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("### 🎯 Recommended Gameplan")

        for tip in f1["gameplan"]:
            st.markdown(
                f"""
                <div style="
                    background:#13283d;
                    color:white; 
                    border-left:5px solid #3b82f6;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {tip}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right_tactical:

        st.markdown(f"### {fighter_two}")

        st.markdown("### ⭐ Primary Weapons")

        for strength in f2["strengths"]:
            st.markdown(
                f"""
                <div style="
                    background:#173322;
                    color:white; 
                    border-left:5px solid #22c55e;
                    color:white;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {strength}
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("### 🚨 Vulnerabilities")

        for weakness in f2["weaknesses"]:
            st.markdown(
                f"""
                <div style="
                    background:#3a2b12;
                    color:white;
                    border-left:5px solid #f59e0b;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {weakness}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### 🎯 Recommended Gameplan")

        for tip in f2["gameplan"]:
            st.markdown(
                f"""
                <div style="
                    background:#13283d;
                    color:white;
                    border-left:5px solid #3b82f6;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    {tip}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ===========================
    # SUMMARY
    # ===========================

    st.subheader("Analyst Summary")
    st.info(summary)

    st.divider()