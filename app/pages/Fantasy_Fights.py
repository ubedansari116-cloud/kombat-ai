import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from src.rag_advisor import KombatAdvisor

st.set_page_config(
    page_title="Fantasy Fight Lab",
    layout="wide"
)

st.title("🥋 Fantasy Fight Lab")

@st.cache_resource
def load_advisor():
    return KombatAdvisor()

advisor = load_advisor()

fighter_names = sorted(advisor.retriever.fighter_names)

left, right = st.columns(2)

with left:
    fighter_one = st.selectbox(
        "Fighter One",
        fighter_names,
        key="fighter_one"
    )

with right:
    fighter_two = st.selectbox(
        "Fighter Two",
        fighter_names,
        index=1 if len(fighter_names) > 1 else 0,
        key="fighter_two"
    )

st.write("---")

if st.button(
    "Load Fighters",
    type="primary",
    use_container_width=True,
):

    fighter_one_data = advisor.load_fighter(fighter_one)
    fighter_two_data = advisor.load_fighter(fighter_two)

    st.session_state["fighter_one_data"] = fighter_one_data
    st.session_state["fighter_two_data"] = fighter_two_data


if (
    "fighter_one_data" in st.session_state
    and
    "fighter_two_data" in st.session_state
):

    st.success("Fighters Loaded Successfully")

    left, right = st.columns(2)

    with left:

        st.subheader(
            st.session_state["fighter_one_data"]["name"]
        )

        st.json(
            st.session_state["fighter_one_data"]["stats"]
        )

    with right:

        st.subheader(
            st.session_state["fighter_two_data"]["name"]
        )

        st.json(
            st.session_state["fighter_two_data"]["stats"]
        )