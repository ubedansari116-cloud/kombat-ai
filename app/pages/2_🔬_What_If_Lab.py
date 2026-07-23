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
    page_icon="🔬",
    layout="wide",
)

@st.cache_resource
def load_advisor():
    return KombatAdvisor()

from fighter_repository import FighterRepository

repository = FighterRepository()

fighter_names = repository.get_all_fighters()

st.title("🔬 What If Lab")

st.caption(
    "Modify a fighter's attributes and instantly see how the predicted outcome changes."
)

st.divider()

left, right = st.columns(2)

with left:

    fighter_one = st.selectbox(
        "Fighter One",
        fighter_names,
        key="fighter_one",
    )

with right:

    fighter_two = st.selectbox(
        "Fighter Two",
        fighter_names,
        key="fighter_two",
    )

from fight_history import FightHistory
history = FightHistory()
advisor = load_advisor()
left, right = st.columns(2)

def reset_fighter_one():

    st.session_state.fighter_one_str_acc = float(
        original_stats_one["striking_accuracy"]
    )

    st.session_state.fighter_one_str_def = float(
        original_stats_one["strike_defense"]
    )

    st.session_state.fighter_one_td_acc = float(
        original_stats_one["takedown_accuracy"]
    )

    st.session_state.fighter_one_td_def = float(
        original_stats_one["takedown_defense"]
    )

    st.session_state.simulation_started = False


def reset_fighter_two():

    st.session_state.fighter_two_str_acc = float(
        original_stats_two["striking_accuracy"]
    )

    st.session_state.fighter_two_str_def = float(
        original_stats_two["strike_defense"]
    )

    st.session_state.fighter_two_td_acc = float(
        original_stats_two["takedown_accuracy"]
    )

    st.session_state.fighter_two_td_def = float(
        original_stats_two["takedown_defense"]
    )

    st.session_state.simulation_started = False

with left:

    version_one = st.radio(
        "Version",
        ["Overall", "Prime", "Debut", "Current"],
        horizontal=True,
        key="version_one",
    )

with right:

    version_two = st.radio(
        "Version",
        ["Overall", "Prime", "Debut", "Current"],
        horizontal=True,
        key="version_two",
    )

if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False

if "last_matchup" not in st.session_state:
    st.session_state.last_matchup = None

current_matchup = (
    fighter_one,
    fighter_two,
    version_one,
    version_two,
)

if st.session_state.last_matchup != current_matchup:
    st.session_state.simulation_started = False
    st.session_state.last_matchup = current_matchup

if version_one == "Overall":
    snapshot_one = None

elif version_one == "Current":
    snapshot_one = history.get_current(fighter_one)
elif version_one == "Prime":
    snapshot_one = history.get_prime(fighter_one)
else:
    snapshot_one = history.get_debut(fighter_one)

if version_two == "Overall":
    snapshot_two = None

elif version_two == "Current":
    snapshot_two = history.get_current(fighter_two)
elif version_two == "Prime":
    snapshot_two = history.get_prime(fighter_two)
else:
    snapshot_two = history.get_debut(fighter_two)

fighter_one_profile = repository.get_fighter(fighter_one)
fighter_two_profile = repository.get_fighter(fighter_two)

stats_one = fighter_one_profile["stats"].copy()
stats_two = fighter_two_profile["stats"].copy()

if snapshot_one is not None:
    stats_one.update(snapshot_one["stats"])

if snapshot_two is not None:
    stats_two.update(snapshot_two["stats"])

import copy

original_stats_one = copy.deepcopy(stats_one)
original_stats_two = copy.deepcopy(stats_two)

if st.session_state.get("loaded_fighter1") != (fighter_one, version_one):

    st.session_state["fighter_one_str_acc"] = stats_one["striking_accuracy"]
    st.session_state["fighter_one_str_def"] = stats_one["strike_defense"]
    st.session_state["fighter_one_td_acc"] = stats_one["takedown_accuracy"]
    st.session_state["fighter_one_td_def"] = stats_one["takedown_defense"]

    st.session_state["loaded_fighter1"] = (fighter_one, version_one)


if st.session_state.get("loaded_fighter2") != (fighter_two, version_two):

    st.session_state["fighter_two_str_acc"] = stats_two["striking_accuracy"]
    st.session_state["fighter_two_str_def"] = stats_two["strike_defense"]
    st.session_state["fighter_two_td_acc"] = stats_two["takedown_accuracy"]
    st.session_state["fighter_two_td_def"] = stats_two["takedown_defense"]

    st.session_state["loaded_fighter2"] = (fighter_two, version_two)
st.subheader("Adjust Attributes")

left, right = st.columns(2)

# ===========================
# Fighter A
# ===========================

with left:

    st.subheader(fighter_one)

    striking_accuracy = st.slider(
        "Striking Accuracy (%)",
        0.0,
        100.0,
        float(stats_one["striking_accuracy"]),
        key="fighter_one_str_acc",
    )

    striking_defense = st.slider(
        "Striking Defense (%)",
        0.0,
        100.0,
        float(stats_one["strike_defense"]),
        key="fighter_one_str_def",
    )

    takedown_accuracy = st.slider(
        "Takedown Accuracy (%)",
        0.0,
        100.0,
        float(stats_one["takedown_accuracy"]),
        key="fighter_one_td_acc",
    )

    takedown_defense = st.slider(
        "Takedown Defense (%)",
        0.0,
        100.0,
        float(stats_one["takedown_defense"]),
        key="fighter_one_td_def",
    )

    stats_one["striking_accuracy"] = striking_accuracy
    stats_one["strike_defense"] = striking_defense
    stats_one["takedown_accuracy"] = takedown_accuracy
    stats_one["takedown_defense"] = takedown_defense

    st.button(
    "Reset Stats",
    key="reset_left",
    use_container_width=True,
    on_click=reset_fighter_one,
)
    

# ===========================
# Fighter B
# ===========================

with right:

    st.subheader(fighter_two)

    fighter_two_striking_accuracy = st.slider(
        "Striking Accuracy (%)",
        0.0,
        100.0,
        float(stats_two["striking_accuracy"]),
        key="fighter_two_str_acc",
    )

    fighter_two_striking_defense = st.slider(
        "Striking Defense (%)",
        0.0,
        100.0,
        float(stats_two["strike_defense"]),
        key="fighter_two_str_def",
    )

    fighter_two_takedown_accuracy = st.slider(
        "Takedown Accuracy (%)",
        0.0,
        100.0,
        float(stats_two["takedown_accuracy"]),
        key="fighter_two_td_acc",
    )

    fighter_two_takedown_defense = st.slider(
        "Takedown Defense (%)",
        0.0,
        100.0,
        float(stats_two["takedown_defense"]),
        key="fighter_two_td_def",
    )

    stats_two["striking_accuracy"] = fighter_two_striking_accuracy
    stats_two["strike_defense"] = fighter_two_striking_defense
    stats_two["takedown_accuracy"] = fighter_two_takedown_accuracy
    stats_two["takedown_defense"] = fighter_two_takedown_defense

    st.button(
        "Reset Stats",
        key="reset_right",
        use_container_width=True,
        on_click=reset_fighter_two,
    )

st.divider()

if "last_matchup" not in st.session_state:
    st.session_state.last_matchup = None

if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False


run = st.button(
    "Run Simulation",
    type="primary",
    use_container_width=True,
)

if run:
    st.session_state.simulation_started = True


if st.session_state.simulation_started:

    result = advisor.predictor.predict(
        fighter_one_name=fighter_one,
        fighter_one_stats=stats_one,
        fighter_two_name=fighter_two,
        fighter_two_stats=stats_two,
    )

    st.success(
        f"Predicted Winner: {result['predicted_winner']}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            fighter_one,
            f"{result['fighter_one_probability']}%"
        )

    with col2:
        st.metric(
            fighter_two,
            f"{result['fighter_two_probability']}%"
        )

    