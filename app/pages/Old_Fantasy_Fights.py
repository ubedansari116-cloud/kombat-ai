import streamlit as st
import sys
import os
from copy import deepcopy

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../..",
        )
    )
)

from src.rag_advisor import KombatAdvisor

st.set_page_config(
    page_title="Kombat AI - Fantasy Fight Lab",
    layout="wide",
)

st.title("🥊 Kombat AI - Fantasy Fight Lab")

st.caption(
    "Create impossible matchups and modify fighter attributes."
)


@st.cache_resource
def load_advisor():
    return KombatAdvisor()


advisor = load_advisor()

fighter_list = sorted(
    advisor.retriever.fighter_names
)


st.subheader("1. Select Matchup")

left, right = st.columns(2)

with left:

    fighter_one = st.selectbox(
        "Fighter One",
        fighter_list,
        key="fantasy_fighter_one",
    )

with right:

    fighter_two = st.selectbox(
        "Fighter Two",
        fighter_list,
        index=1 if len(fighter_list) > 1 else 0,
        key="fantasy_fighter_two",
    )


mutable_fields = {
    "striking_accuracy": "Striking Accuracy",
    "strike_defense": "Strike Defence",
    "takedown_accuracy": "Takedown Accuracy",
    "takedown_defense": "Takedown Defence",
    "submission_avg": "Submission Average",
}


st.divider()

st.subheader("2. Load Fighter Profiles")

if st.button(
    "Load Fighter Profiles",
    type="primary",
    use_container_width=True,
):

    try:

        fighter_one_data = advisor.load_fighter(
            fighter_one,
        )

        fighter_two_data = advisor.load_fighter(
            fighter_two,
        )

        st.session_state.f1_loaded_stats = deepcopy(
            fighter_one_data["stats"]
        )

        st.session_state.f2_loaded_stats = deepcopy(
            fighter_two_data["stats"]
        )

        st.session_state.loaded_matchup = (
            f"{fighter_one}_vs_{fighter_two}"
        )

        st.success(
            "Profiles loaded successfully."
        )

    except Exception as e:

        st.error(e)

current_matchup = f"{fighter_one}_vs_{fighter_two}"

if (
    "loaded_matchup" in st.session_state
    and st.session_state.loaded_matchup != current_matchup
):

    st.session_state.pop("f1_loaded_stats", None)
    st.session_state.pop("f2_loaded_stats", None)
    st.session_state.pop("loaded_matchup", None)


if (
    "f1_loaded_stats" in st.session_state
    and "f2_loaded_stats" in st.session_state
):

    st.divider()

    st.subheader("3. Modify Fighter Attributes")

    fighter_one_stats = deepcopy(
        st.session_state.f1_loaded_stats
    )

    fighter_two_stats = deepcopy(
        st.session_state.f2_loaded_stats
    )

    left, right = st.columns(2)

    with left:

        st.markdown(f"### 🔴 {fighter_one}")

        for key, label in mutable_fields.items():

            fighter_one_stats[key] = st.slider(

                label,

                min_value=0.0,

                max_value=100.0,

                value=float(fighter_one_stats[key]),

                key=f"f1_{key}",
            )

    with right:

        st.markdown(f"### 🔵 {fighter_two}")

        for key, label in mutable_fields.items():

            fighter_two_stats[key] = st.slider(

                label,

                min_value=0.0,

                max_value=100.0,

                value=float(fighter_two_stats[key]),

                key=f"f2_{key}",
            )

    st.divider()
# ===========================
# RUN SIMULATION
# ===========================

if st.button(
    "Initialize Simulation",
    type="primary",
    use_container_width=True,
):

    with st.spinner("Running Fantasy Fight..."):

        try:

            simulation = advisor.what_if_simulator.simulate(

                fight_engine=advisor.fight_engine,

                fighter_one_name=fighter_one,
                fighter_one_stats=fighter_one_stats,

                fighter_two_name=fighter_two,
                fighter_two_stats=fighter_two_stats,

            )
            

            st.session_state["simulation"] = simulation

        except Exception as e:

            st.error(
                f"Simulation Error:\n\n{e}"
            )


if "simulation" in st.session_state:

    simulation = st.session_state["simulation"]

    st.divider()

    st.subheader("🧠 Fight IQ Results")

    left, right = st.columns(2)

    with left:

        st.metric(

            fighter_one,

            simulation["fighter_one"]["grade"],

            f'{simulation["fighter_one"]["fight_iq"]:.1f} Fight IQ',

        )

        st.success("Strengths")

        for strength in simulation["fighter_one"]["strengths"]:

            st.write(f"✅ {strength}")

        st.warning("Weaknesses")

        for weakness in simulation["fighter_one"]["weaknesses"]:

            st.write(f"⚠️ {weakness}")

    with right:

        st.metric(

            fighter_two,

            simulation["fighter_two"]["grade"],

            f'{simulation["fighter_two"]["fight_iq"]:.1f} Fight IQ',

        )

        st.success("Strengths")

        for strength in simulation["fighter_two"]["strengths"]:

            st.write(f"✅ {strength}")

        st.warning("Weaknesses")

        for weakness in simulation["fighter_two"]["weaknesses"]:

            st.write(f"⚠️ {weakness}")

    st.divider()

    st.subheader("🥊 Matchup Intelligence")

    for insight in simulation["matchup_analysis"]:

        st.info(insight)

    st.success(

        f"Overall Edge: {simulation['overall_edge']}"

    )