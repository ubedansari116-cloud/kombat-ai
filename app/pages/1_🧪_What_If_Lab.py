import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from rag_advisor import KombatAdvisor


st.set_page_config(
    page_title="What If Lab",
    page_icon="🧪",
    layout="wide",
)


@st.cache_resource
def load_advisor():
    return KombatAdvisor()


advisor = load_advisor()
if "lab_result" not in st.session_state:
    st.session_state.lab_result = None

st.title("🧪 What If Lab")
st.caption("Simulate hypothetical changes to fighter attributes.")

fighter_names = sorted(advisor.retriever.fighter_names)

left, right = st.columns(2)

with left:

    fighter_one = st.selectbox(
        "Fighter One",
        fighter_names,
    )

with right:

    fighter_two = st.selectbox(
        "Fighter Two",
        fighter_names,
        index=1,
    )

load = st.button(
    "Load Fighters",
    type="primary",
    use_container_width=True,
)

if load:

    query = f"Compare {fighter_one} and {fighter_two}"

    st.session_state.lab_result = advisor.answer(query)
if st.session_state.lab_result is None:
    st.stop()

result = st.session_state.lab_result

st.subheader("Adjust Fighter Attributes")

left_stats, right_stats = st.columns(2)
fighter_one_stats = result["fighters"][0]["stats"]
fighter_two_stats = result["fighters"][1]["stats"]

with left_stats:

    st.markdown(f"## {fighter_one}")

    f1_striking = st.slider(
        "Striking Accuracy",
        20,
        80,
        int(fighter_one_stats["striking_accuracy"]),
    )

    f1_td_acc = st.slider(
        "Takedown Accuracy",
        0,
        100,
        int(fighter_one_stats["takedown_accuracy"]),
    )

    f1_td_def = st.slider(
        "Takedown Defence",
        0,
        100,
        int(fighter_one_stats["takedown_defense"]),
    )

with right_stats:

    st.markdown(f"## {fighter_two}")

    f2_striking = st.slider(
        "Striking Accuracy",
        20,
        80,
        int(fighter_two_stats["striking_accuracy"]),
        key="f2_strike",
    )

    f2_td_acc = st.slider(
        "Takedown Accuracy",
        0,
        100,
        int(fighter_two_stats["takedown_accuracy"]),
        key="f2_td_acc",
    )

    f2_td_def = st.slider(
        "Takedown Defence",
        0,
        100,
        int(fighter_two_stats["takedown_defense"]),
        key="f2_td_def",
    )
st.write("")

_, center, _ = st.columns([1, 2, 1])

with center:
    run = st.button(
        "🧪 Run Simulation",
        use_container_width=True,
    )
    if run:

        simulation = advisor.what_if_simulator.simulate(

           fight_engine=advisor.fight_engine,

           fighter_one_name=fighter_one,
            fighter_one_stats=fighter_one_stats,

            fighter_two_name=fighter_two,
            fighter_two_stats=fighter_two_stats,

            fighter_one_changes={
                "striking_accuracy": float(f1_striking),
                "takedown_accuracy": float(f1_td_acc),
                "takedown_defense": float(f1_td_def),
           },

           fighter_two_changes={
                "striking_accuracy": float(f2_striking),
                   "takedown_accuracy": float(f2_td_acc),
                "takedown_defense": float(f2_td_def),
          },

        )

        st.divider()

        st.subheader("😮 Updated Fight IQ")

        left_result, right_result = st.columns(2)

        with left_result:

            st.metric(
                fighter_one,
                simulation["fighter_one"]["grade"],
                f'{simulation["fighter_one"]["fight_iq"]:.1f}',
        )

            st.success("Strengths")

            for strength in simulation["fighter_one"]["strengths"]:
                st.write(f"😝 {strength}")

            st.warning("Weaknesses")

            for weakness in simulation["fighter_one"]["weaknesses"]:
                st.write(f"😩 {weakness}")

        with right_result:

            st.metric(
                fighter_two,
                simulation["fighter_two"]["grade"],
                f'{simulation["fighter_two"]["fight_iq"]:.1f}',
        )

            st.success("Strengths")

            for strength in simulation["fighter_two"]["strengths"]:
                st.write(f"😝 {strength}")

            st.warning("Weaknesses")

            for weakness in simulation["fighter_two"]["weaknesses"]:
                st.write(f"😩 {weakness}")

        st.divider()

        st.subheader("🥀 Updated Matchup Intelligence")

        for insight in simulation["matchup_analysis"]:
            st.info(insight)

        st.success(
            f"Fight IQ Edge: {simulation['overall_edge']}"
    )