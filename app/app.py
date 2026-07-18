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
st.caption("AI-powered UFC matchup analysis and fight prediction")

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
        # SUMMARY
        # ===========================

    st.subheader("Analyst Summary")
    st.info(summary)

    st.divider()

        # ===========================
        # COMPARISON TABLE
        # ===========================

    st.subheader("Statistical Comparison")

    comparison_rows = []

    for item in comparison["advantages"]:
            comparison_rows.append(
                {
                    "Metric": item["metric"],
                    fighter_one: item["fighter_one_value"],
                    fighter_two: item["fighter_two_value"],
                    "Advantage": item["winner"],
                }
            )

    comparison_dataframe = pd.DataFrame(comparison_rows)

    st.dataframe(
            comparison_dataframe,
            use_container_width=True,
            hide_index=True,
        )