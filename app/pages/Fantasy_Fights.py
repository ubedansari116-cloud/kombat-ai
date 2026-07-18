import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.rag_advisor import KombatAdvisor

st.set_page_config(page_title="Kombat AI - Fantasy Fight Lab", layout="wide")

st.title("🥋 Kombat AI: Fantasy Fight Lab")
st.markdown("Run counterfactual 'What-If' simulations by mutating live fighter attributes.")

# 1. Initialize Advisor Core
@st.cache_resource
def load_advisor():
    return KombatAdvisor()

try:
    advisor = load_advisor()
    fighter_list = sorted(list(advisor.retriever.fighter_names))
except Exception as e:
    st.error(f"Failed to load Kombat Engine dependencies: {e}")
    st.stop()

# 2. Matchup Selection
st.subheader("1. Select Matchup")
col_a, col_b = st.columns(2)

with col_a:
    fighter_one = st.selectbox("Select Fighter One (Red)", options=fighter_list, key="f1_select")
with col_b:
    fighter_two = st.selectbox("Select Fighter Two (Blue)", options=fighter_list, key="f2_select")

# Define our target core metrics
mutable_fields = [
    "Striking_Accuracy", "Striking_Defense", 
    "Takedown_Accuracy", "Takedown_Defense", 
    "Submission_Avg", "Stamina", "Fight_IQ"
]

# --- REPLACE FROM HERE (Updated Cleaner & Fallback Loader) ---
def clean_extracted_stats(raw_stats):
    cleaned = {}
    for field in mutable_fields:
        # Check if the field exists and is not None
        val = raw_stats.get(field) if raw_stats else None
        
        if val is None or val == "" or str(val).strip().lower() == "none":
            # Direct fallback: set to 50.0 so the sliders don't crash
            cleaned[field] = 50.0
        else:
            try:
                cleaned[field] = float(val)
            except ValueError:
                cleaned[field] = 50.0
    return cleaned

# 3. Step 2: Load Stats explicitly into Session State
st.markdown("---")
st.subheader("2. Load Profile Data")

if st.button("Load Fighter Profiles", type="secondary"):
    with st.spinner("Extracting RAG baseline records..."):
        f1_raw = advisor.extract_stats(fighter_one)
        f2_raw = advisor.extract_stats(fighter_two)
        
        # Check if the RAG parser failed completely (returned empty dict or None)
        is_f1_null = not f1_raw or all(v is None for v in f1_raw.values())
        is_f2_null = not f2_raw or all(v is None for v in f2_raw.values())
        
        if is_f1_null or is_f2_null:
            st.warning(
                "⚠️ Note: The RAG engine extracted text documents, but the regular expression parser "
                "could not map the document text into attributes. Initializing sliders with baseline averages (50.0). "
                "You can still manually adjust these sliders below to test your simulation!"
            )
        else:
            st.success(f"Successfully loaded profiles for {fighter_one} and {fighter_two}!")
            
        # Scrub data to ensure no NoneType values sneak past into calculations
        st.session_state.f1_loaded_stats = clean_extracted_stats(f1_raw)
        st.session_state.f2_loaded_stats = clean_extracted_stats(f2_raw)
        st.session_state.loaded_matchup = f"{fighter_one}_vs_{fighter_two}"
# --- TO HERE ---

# Clear state if the user picks entirely new fighters in the drop downs
current_matchup = f"{fighter_one}_vs_{fighter_two}"
if "loaded_matchup" in st.session_state and st.session_state.loaded_matchup != current_matchup:
    if "f1_loaded_stats" in st.session_state: del st.session_state.f1_loaded_stats
    if "f2_loaded_stats" in st.session_state: del st.session_state.f2_loaded_stats
    if "loaded_matchup" in st.session_state: del st.session_state.loaded_matchup

# 4. Step 3: Display Sliders only after profiles are loaded
if "f1_loaded_stats" in st.session_state and "f2_loaded_stats" in st.session_state:
    st.markdown("---")
    st.subheader("3. Adjust Performance Vectors")
    
    col1, col2 = st.columns(2)
    
    f1_mutated = {}
    with col1:
        st.markdown(f"### 🔴 {fighter_one} Modifiers")
        for field in mutable_fields:
            base_val = st.session_state.f1_loaded_stats[field]
            f1_mutated[field] = st.slider(
                f"{field.replace('_', ' ')}", 
                min_value=0.0, max_value=100.0, 
                value=base_val, 
                key=f"slider_f1_{field}"
            )
            
    f2_mutated = {}
    with col2:
        st.markdown(f"### 🔵 {fighter_two} Modifiers")
        for field in mutable_fields:
            base_val = st.session_state.f2_loaded_stats[field]
            f2_mutated[field] = st.slider(
                f"{field.replace('_', ' ')}", 
                min_value=0.0, max_value=100.0, 
                value=base_val, 
                key=f"slider_f2_{field}"
            )

    # 5. Step 4: Run Simulation Engine
    st.markdown("---")
    if st.button("Initialize Simulation", type="primary"):
        with st.spinner("Processing tactical differentials..."):
            try:
                sim_result = advisor.what_if_simulator.simulate(
                    advisor.fight_engine,
                    fighter_one_name=fighter_one,
                    fighter_two_name=fighter_two,
                    fighter_one_stats=f1_mutated,
                    fighter_two_stats=f2_mutated
                )
                
                st.success("Simulation Computed Successfully!")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric(
                        label=f"{fighter_one} Probability", 
                        value=f"{sim_result.get('fighter_one_probability', 0.0):.1%}"
                    )
                with res_col2:
                    st.metric(
                        label=f"{fighter_two} Probability", 
                        value=f"{sim_result.get('fighter_two_probability', 0.0):.1%}"
                    )
                    
                if "insights" in sim_result:
                    st.markdown("### 📋 Tactical Matchup Insights")
                    for insight in sim_result["insights"]:
                        st.info(insight)
                        
            except Exception as sim_err:
                st.error(f"Execution Error inside simulator module: {sim_err}")
else:
    st.info("💡 Please click the 'Load Fighter Profiles' button above to extract data and reveal the mutation controls.")