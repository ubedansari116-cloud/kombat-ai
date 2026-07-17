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


st.set_page_config(
    page_title="Kombat AI",
    page_icon="🥰",
    layout="wide",
)


@st.cache_resource
def load_advisor():
    return KombatAdvisor()


advisor = load_advisor()


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
        st.warning("Select two different fighters.")

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

        st.divider()

        st.subheader("Fight Prediction")

        winner_column, probability_one_column, probability_two_column = st.columns(3)

        with winner_column:
            st.metric(
                "Predicted Winner",
                predicted_winner,
            )

        with probability_one_column:
            st.metric(
                fighter_one,
                f"{fighter_one_probability:.1f}%",
            )

        with probability_two_column:
            st.metric(
                fighter_two,
                f"{fighter_two_probability:.1f}%",
            )

        st.subheader("Analyst Summary")
        st.write(summary)

        st.subheader("Statistical Comparison")

        advantages = comparison["advantages"]
        
        comparison_rows = []
        
        for item in advantages:
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