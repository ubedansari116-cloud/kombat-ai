# 🥊 Kombat AI
### Explainable AI Platform for UFC Fight Prediction & Tactical Analysis

Kombat AI is an end-to-end artificial intelligence platform built for analysing UFC matchups using machine learning, explainable AI, tactical reasoning, retrieval-augmented generation (RAG), and large language models.

Unlike traditional prediction systems that only output a winner, Kombat AI explains **why** a fighter is favoured, highlights stylistic advantages, simulates fight momentum across five rounds, recommends tactical gameplans, and allows users to modify fighter attributes to analyse hypothetical scenarios.

---

# Live Application

https://kombat-ai.streamlit.app

---

# Repository

https://github.com/ubedansari116-cloud/kombat-ai

---

# Table of Contents

- Overview
- Features
- Architecture
- Machine Learning Pipeline
- Tactical Analysis Engine
- Explainable AI
- RAG Knowledge Base
- AI Coach
- What If Lab
- Confidence Engine
- Recommendation Engine
- Project Structure
- Technologies Used
- Installation
- Future Improvements

---

# Overview

Mixed Martial Arts is an extremely complex sport.

Winning is influenced by:

- striking ability
- wrestling
- grappling
- cardio
- durability
- experience
- stylistic matchup
- pace
- fight IQ

Most prediction systems reduce this into a single probability.

Kombat AI instead models the fight from multiple perspectives to generate:

- winner prediction
- confidence score
- tactical explanation
- fight attribute comparison
- radar visualisation
- momentum progression
- gameplan recommendations
- fighter-specific AI coaching

The objective was to create a system that feels closer to how a professional analyst breaks down a fight.

---
# 🚀 Key Innovations

Unlike conventional fight prediction models that only output a winner, Kombat AI was designed as a complete explainable combat intelligence platform.

### 🧠 Explainable Predictions
Predictions are accompanied by tactical reasoning, confidence analysis, fighter attribute comparisons, and momentum simulations, making every result interpretable rather than a black-box output.

---

### 🎯 Tactical Intelligence Engine
Instead of relying solely on machine learning probabilities, the platform derives combat attributes such as Power, Durability, Fight IQ, Wrestling, Grappling, and Cardio from real fighter statistics to generate matchup-specific game plans and strategic insights.

---

### 📈 Dynamic Momentum Simulation
A custom momentum engine simulates how fights evolve across five rounds by modelling striking exchanges, ground control, fatigue, cardio, and stylistic advantages, producing realistic round-by-round momentum shifts.

---

### 🤖 Retrieval-Augmented AI Coach
The AI Coach combines:
- Machine Learning predictions
- Fighter-specific knowledge documents
- Vector similarity search
- Google Gemini

to answer contextual questions with grounded responses instead of generic LLM outputs.

---

### 🔬 Interactive What-If Analysis
Users can modify fighter attributes such as striking accuracy, takedown defence, cardio, or Fight IQ and instantly observe how those changes affect prediction outcomes, tactical analysis, and confidence scores.

---

### 📊 Advanced Visual Analytics
The platform includes multiple explainable visualisations, including:
- Fighter Radar Charts
- Attribute Comparison Charts
- Round-by-Round Momentum Graphs
- Ground Control Analysis
- Tactical Breakdown Cards

allowing users to understand not only *who* wins, but *why* they win.

---

### ⚙️ Modular AI Architecture
The project is built as independent analytical engines that work together:

- Prediction Engine
- Confidence Engine
- Explainability Engine
- Tactical Recommendation Engine
- Momentum Engine
- Fight History Engine
- RAG Advisor
- AI Coach

This modular design makes the platform scalable and allows new analytical components to be integrated without affecting the existing system.

---

### 🧩 Hybrid AI Decision Pipeline

Kombat AI combines multiple artificial intelligence paradigms into a single decision-making system instead of relying on a standalone prediction model.

The platform integrates:

- **Machine Learning** – Random Forest classifier for winner prediction.
- **Feature Engineering** – Custom combat metrics derived from raw UFC statistics.
- **Rule-Based Reasoning** – Tactical analysis, momentum simulation, and matchup evaluation.
- **Retrieval-Augmented Generation (RAG)** – Fighter-specific knowledge retrieval using vector similarity search.
- **Large Language Models (Google Gemini)** – Context-aware coaching, explanations, and strategic recommendations.
- **Interactive Simulation** – Real-time recalculation of predictions through the What-If Lab.

By combining predictive analytics, explainable AI, retrieval systems, and generative AI, Kombat AI delivers a layered decision-making process that mirrors how professional analysts evaluate fights rather than simply predicting an outcome.

---

# Features

## 🧠 AI Fight Prediction

Uses a trained Random Forest classifier to predict fight winners using engineered fighter statistics.

Outputs:

- predicted winner
- win probability
- confidence score

---

## 📊 Fighter Attribute Comparison

Generates mirrored attribute comparisons for:

- Power
- Accuracy
- Durability
- Wrestling
- Grappling
- Cardio
- Fight IQ

Winning attributes are highlighted automatically.

---

## 📈 Radar Analysis

Creates radar charts that compare fighter strengths across multiple combat dimensions.

---

## 🎯 Tactical Breakdown

Automatically generates:

### Primary Weapons

Examples:

- Excellent physical tools
- Elite striking accuracy
- Dangerous wrestling
- High pace

### Vulnerabilities

Examples:

- Vulnerable to takedowns
- Limited submission threat
- Low striking defence

### Recommended Gameplan

Examples:

- Keep the fight standing
- Mix in takedowns
- Pressure against the cage
- Counter patiently

---

## 📉 Momentum Engine

Simulates fight momentum over five rounds.

Two independent systems are generated:

- Stand-up momentum
- Ground control momentum

Momentum changes dynamically using:

- initial technical advantage
- fatigue
- cardio
- fighting style
- round-to-round momentum

---

## 🤖 AI Coach

An interactive assistant capable of answering questions such as:

- How does Islam beat Charles?
- Why is Pereira dangerous?
- What are Merab's weaknesses?

The AI combines:

- Machine Learning prediction
- Tactical analysis
- Fighter documents
- Gemini LLM reasoning

---

## 🔬 What If Lab

Allows users to modify fighter attributes before simulation.

Examples:

- Increase striking accuracy
- Improve takedown defence
- Reduce cardio
- Increase Fight IQ

The prediction engine immediately recalculates:

- winner
- probabilities
- tactical analysis
- confidence

---

# Architecture

```
                   Fighter Statistics
                          │
                          ▼
                 Feature Engineering
                          │
                          ▼
              Random Forest Classifier
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Winner Prediction   Confidence Engine   Tactical Scores
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
               Explainability Engine
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Radar Charts     Momentum Engine     Attribute Charts
                          │
                          ▼
                  Streamlit Frontend
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
      AI Coach       What If Lab      Tactical Breakdown
```

---

# Machine Learning Pipeline

## Dataset

The model was trained using historical UFC fighter statistics including:

- Significant Strikes Landed per Minute
- Significant Strikes Absorbed
- Strike Accuracy
- Strike Defence
- Takedown Average
- Takedown Accuracy
- Takedown Defence
- Submission Average
- Wins
- Losses
- Reach
- Height
- Age
- Weight

---

## Feature Engineering

Raw statistics were transformed into meaningful combat indicators.

Examples:

- striking differential
- offensive pressure
- defensive efficiency
- grappling effectiveness
- durability estimate

---

## Model

Random Forest Classifier

Chosen because it:

- handles nonlinear relationships
- works well with structured data
- reduces overfitting
- provides stable predictions
- performs well without extensive scaling

---

# Tactical Analysis Engine

Every fighter receives calculated tactical attributes.

Examples:

Power

```
Power = SPLM × scaling factor
```

Durability

```
Strike Defence
+
Damage Absorption
```

Fight IQ

Combination of:

- striking accuracy
- defence
- wrestling efficiency
- offensive output
- defensive output

These derived values power almost every visualisation inside the application.

---

# Explainable AI

Rather than only predicting a winner, Kombat AI explains:

- WHY a fighter is favoured
- Which attributes created the prediction
- Tactical strengths
- Tactical weaknesses
- Confidence level
- Momentum progression

This transforms the prediction into a genuine fight analysis.

---

# Confidence Engine

The confidence score is not a model probability.

Instead it combines:

- prediction probability
- attribute gap
- matchup dominance
- statistical separation

This produces more realistic confidence levels.

---

# Recommendation Engine

Creates fight-specific tactical recommendations.

Examples:

- Keep the fight standing
- Mix in wrestling
- Attack the body
- Pressure early
- Slow the pace

Recommendations change based on the opponent.

---

# RAG Knowledge Base

Every fighter has an individual knowledge document.

The pipeline:

```
Question

↓

Sentence Transformer Embedding

↓

Vector Similarity Search

↓

Relevant Fighter Documents

↓

Gemini

↓

Final Response
```

This ensures responses are grounded in fighter-specific information instead of generic LLM knowledge.

---

# AI Coach

The AI Coach combines multiple systems.

Inputs:

- Machine Learning prediction
- Tactical analysis
- Fighter knowledge base
- Gemini LLM

Outputs:

- matchup explanations
- strategic advice
- fighter strengths
- weaknesses
- historical context

---

# What If Lab

The What If Lab enables hypothetical scenarios.

Example:

"What if Alex Pereira improved his takedown defence?"

The application updates:

- tactical attributes
- prediction
- confidence
- explanations
- charts

without retraining the model.

---

# Project Structure

```
kombat-ai/

│

├── app/

│ ├── app.py

│ └── pages/

│ ├── AI_Coach.py

│ └── What_If_Lab.py

│

├── src/

│ ├── predictor.py

│ ├── fight_engine.py

│ ├── confidence_engine.py

│ ├── explainability_engine.py

│ ├── recommendation_engine.py

│ ├── rag_advisor.py

│ ├── rag_retriever.py

│ ├── ai_coach.py

│ ├── llm_coach.py

│ ├── radar.py

│ ├── fighter_repository.py

│ └── fight_history.py

│

├── models/

├── data/

├── fighter_docs/

└── README.md
```

---

# Technologies Used

## Languages

- Python
- SQL
- HTML
- CSS
- JavaScript

## Machine Learning

- Scikit-Learn
- Random Forest

## AI

- Google Gemini
- Sentence Transformers
- Retrieval Augmented Generation

## Data

- Pandas
- NumPy

## Visualisation

- Matplotlib
- Streamlit

## Backend

- Supabase

## Version Control

- Git
- GitHub

---

# Installation

Clone the repository

```bash
git clone https://github.com/ubedansari116-cloud/kombat-ai.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Add your Gemini API key inside Streamlit Secrets or `.env`:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app/app.py
```

---

# Future Improvements

- Ensemble machine learning models
- Live UFC statistics integration
- Betting odds analysis
- Fighter clustering
- Event simulation
- Agentic AI coaching
- Fight timeline simulation
- Historical matchup retrieval

---

# Author

**Ubed Ansari**

GitHub

https://github.com/ubedansari116-cloud

Email

ubedansari116@gmail.com