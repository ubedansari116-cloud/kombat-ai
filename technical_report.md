# Kombat AI
## Technical Design & System Documentation

**Version:** 1.0

**Author:** Ubed Ansari

---

# Table of Contents

1. Introduction
2. System Architecture
3. Data Pipeline
4. Machine Learning Pipeline
5. Application Workflow
6. Main Application (`app.py`)
7. What If Lab
8. AI Coach
9. Deployment
10. Engineering Decisions
11. Future Improvements

---

# 1. Introduction

## Purpose

Kombat AI is an explainable artificial intelligence platform designed to analyse UFC matchups using machine learning, statistical modelling, retrieval-augmented generation (RAG), and large language models.

Unlike conventional fight prediction systems that only predict the winner of a matchup, Kombat AI attempts to replicate the analytical reasoning process used by professional fight analysts.

The platform predicts fight outcomes while simultaneously explaining the tactical reasons behind those predictions through fighter comparisons, radar analysis, momentum simulations, confidence estimation, tactical recommendations, and AI-generated coaching.

---

## Objectives

The primary objectives of Kombat AI are:

- Predict UFC fight outcomes using historical fighter statistics.
- Provide transparent and explainable predictions rather than black-box outputs.
- Visualise fighter strengths and weaknesses through interactive analytics.
- Simulate how a fight evolves over multiple rounds.
- Allow users to experiment with hypothetical fighter improvements.
- Generate fighter-specific coaching responses using Retrieval-Augmented Generation (RAG) and Google Gemini.

---

## Scope

The current implementation focuses exclusively on professional UFC fighters.

The application currently supports:

- Fight prediction
- Tactical breakdown generation
- Fighter attribute comparison
- Radar visualisation
- Momentum simulation
- Confidence estimation
- AI coaching
- Interactive "What If" simulations

Future versions may support additional combat sports including boxing, kickboxing, and Muay Thai.

---

## Design Philosophy

Kombat AI was designed around four engineering principles:

### Explainability

Every prediction should be accompanied by sufficient reasoning for users to understand why the prediction was made.

---

### Modularity

Each analytical component should operate independently, allowing future systems to be added without affecting existing functionality.

---

### Reproducibility

Every prediction should be generated from deterministic statistical calculations and reproducible machine learning outputs.

---

### User Interaction

The platform should allow users not only to analyse existing fighters but also to explore hypothetical scenarios by modifying fighter attributes and observing the resulting changes.

---

# 2. System Architecture

## Overview

Kombat AI follows a modular architecture where each subsystem performs a specialised task.

Rather than combining all analytical logic into a single model, independent engines collaborate to produce the final analysis.

The prediction model determines the likely winner, while additional engines explain, visualise, and contextualise that prediction.

---

## System Architecture


                                               User
                                                │
                                                ▼
                                        Streamlit Interface
                                                │
                                                ▼
                                    KombatAdvisor (Central Orchestrator)
                                                │
                                ─────────────────────────────────────────────
                               │                                             │
                               ▼                                             ▼
                            Prediction Engine                     Fighter Repository

                            (Random Forest)                             (CSV Dataset)
                                │                                             │
                                ▼                                             ▼
                            Fight Engine                      Fight History Engine
                               │                                             │
                                ─────────────────────────────────────────────
                                                    │
                                                    ▼
                                            Confidence Engine
                                                    │
                                                    ▼
                                            Recommendation Engine
                                                    │
                                                    ▼
                                            Explainability Engine
                                                    │
                                            ───────────────────────
                                           │                       │
                                           ▼                       ▼
                                        Radar Engine      Momentum Engine
                                           │                       │
                                            ───────────────────────
                                                    │
                                                    ▼
                                             Visual Interface


---

## Component Responsibilities

### Streamlit Interface

The Streamlit frontend is responsible for user interaction.

Its responsibilities include:

- fighter selection
- prediction requests
- displaying visualisations
- rendering analytical outputs
- navigation between application pages

---

### KombatAdvisor

KombatAdvisor acts as the central controller of the application.

It coordinates communication between all analytical modules.

Responsibilities include:

- loading the prediction model
- retrieving fighter statistics
- generating predictions
- combining outputs from multiple analytical engines
- returning a complete fight analysis

---

### Prediction Engine

The Prediction Engine performs winner prediction using a trained Random Forest classifier.

Outputs include:

- predicted winner
- prediction probability

This engine does not generate explanations.

Those responsibilities are delegated to downstream analytical modules.

---

### Fighter Repository

The Fighter Repository serves as the primary data source for the application.

Instead of querying an online database, all fighter statistics are loaded from locally stored CSV datasets.

Responsibilities include:

- loading fighter statistics
- returning fighter profiles
- retrieving historical performance data
- supplying inputs for every analytical engine

---

### Fight Engine

The Fight Engine converts raw fighter statistics into meaningful combat metrics.

These derived metrics power:

- radar charts
- attribute comparisons
- tactical analysis
- momentum simulation
- recommendation generation

The Fight Engine forms the analytical core of the application.

---

### Confidence Engine

The Confidence Engine transforms raw prediction probabilities into more interpretable confidence estimates.

Confidence considers both:

- machine learning certainty
- statistical separation between fighters

---

### Recommendation Engine

The Recommendation Engine generates strategic recommendations tailored to the selected matchup.

Recommendations are based on fighter strengths, weaknesses, and stylistic interactions.

---

### Explainability Engine

The Explainability Engine converts statistical outputs into human-readable tactical insights.

Examples include:

- primary weapons
- vulnerabilities
- stylistic advantages
- recommended fight plans

---

### Radar Engine

Generates radar visualisations representing fighter strengths across multiple combat attributes.

---

### Momentum Engine

Simulates how a fight evolves over five rounds.

Separate simulations are produced for:

- striking momentum
- ground control momentum

Momentum changes according to fighter statistics, fatigue, and stylistic modifiers.

---

# 3. Data Pipeline

## Overview

The performance of Kombat AI depends heavily on the quality and organisation of its underlying data.

Rather than relying on external APIs or live databases, the platform uses locally stored datasets that are cleaned, structured, and transformed into formats suitable for machine learning and Retrieval-Augmented Generation (RAG).

This approach provides:

- Faster prediction times
- Complete reproducibility
- Offline functionality
- Greater control over preprocessing
- Easier future expansion

---

## Data Sources

The application uses multiple datasets, each serving a specific purpose within the system.

| Dataset | Purpose |
|---------|---------|
| UFC.csv | Primary fighter statistics used by the prediction engine |
| fighter_details.csv | Extended fighter metadata and profile information |
| fight_details.csv | Historical fight-level statistics |
| event_details.csv | UFC event information |
| ufc-fighters-statistics.csv | Additional fighter performance metrics |

---

## Primary Dataset (UFC.csv)

The primary dataset contains the statistical information required by the machine learning model.

Each fighter record includes offensive, defensive, and grappling statistics that are later transformed into higher-level combat attributes.

Important features include:

- Wins
- Losses
- Significant Strikes Landed per Minute (SLpM)
- Significant Strikes Absorbed per Minute (SApM)
- Striking Accuracy
- Strike Defence
- Takedown Average
- Takedown Accuracy
- Takedown Defence
- Submission Average
- Reach
- Stance
- Height
- Weight Class

These statistics serve as the foundation for both prediction and analytical visualisations.

---

## Secondary Datasets

Additional datasets are used to enrich fighter information throughout the application.

These datasets provide:

- detailed fighter profiles
- historical fight records
- event information
- supplementary statistical context

Although not every dataset is directly consumed by the prediction model, they support analytical features and future extensibility.

---

## Fighter Repository

The `FighterRepository` module acts as the application's central data access layer.

Instead of allowing every engine to read CSV files independently, all fighter information passes through this repository.

Responsibilities include:

- Loading fighter datasets
- Retrieving fighter statistics
- Returning fighter profiles
- Searching fighters
- Providing data to downstream analytical engines

Centralising data access improves maintainability and prevents duplicate loading logic throughout the application.

---

## Data Loading Process

The application follows a simple but efficient loading pipeline.


CSV Files

↓

Pandas DataFrames

↓

Fighter Repository

↓

Prediction Engine

Fight Engine

AI Coach

What If Lab


Datasets are loaded only when required and subsequently reused by the application to reduce unnecessary file operations.

---

## Data Preprocessing

Before being used for prediction or analysis, fighter data undergoes preprocessing.

This includes:

- Handling missing values
- Converting percentages into numerical values
- Standardising feature formats
- Removing invalid records where necessary
- Preparing machine learning feature vectors

These preprocessing steps ensure consistent model behaviour regardless of the original dataset formatting.

---

## Feature Selection

Not every available statistic contributes equally to prediction quality.

Only statistically meaningful features are retained for the Random Forest model.

Selected features focus primarily on:

- Offensive striking
- Defensive striking
- Wrestling effectiveness
- Grappling effectiveness
- Overall fight experience

The final feature list used during inference is stored alongside the trained model to guarantee consistency between training and prediction.

---

## Knowledge Base for AI Coach

The AI Coach operates using Retrieval-Augmented Generation (RAG).

Rather than relying solely on a Large Language Model, Kombat AI maintains a structured knowledge base containing fighter-specific documents.

Each fighter has an associated knowledge document describing:

- Fighting style
- Strengths
- Weaknesses
- Career achievements
- Tactical tendencies
- Historical performance

These documents are stored inside the `fighter_docs/` directory.

---

## Embedding Generation

Each knowledge document is converted into dense vector representations using Sentence Transformers.

This process converts human-readable text into numerical embeddings suitable for semantic similarity search.

Pipeline:


Fighter Documents

↓

Sentence Transformer

↓

Vector Embeddings

↓

Vector Store


Embedding generation is performed once during preprocessing and reused during runtime.

---

## Retrieval-Augmented Generation Pipeline

When a user asks the AI Coach a question, the following workflow is executed.


User Question

↓

Sentence Embedding

↓

Similarity Search

↓

Relevant Fighter Documents

↓

Prompt Construction

↓

Gemini

↓

Final Response


This ensures that AI-generated responses remain grounded in fighter-specific information rather than relying exclusively on general language model knowledge.

---

## Advantages of the Data Pipeline

The current pipeline provides several engineering benefits.

- Fully offline fighter statistics
- Deterministic predictions
- Fast inference
- Easy dataset replacement
- Modular architecture
- Reproducible machine learning workflow
- Efficient semantic retrieval for AI coaching

This modular design also simplifies future integration of additional combat sports without requiring significant architectural changes.

# 4. Machine Learning Pipeline

## Overview

The machine learning component of Kombat AI is responsible for predicting the most likely winner of a UFC matchup.

Rather than attempting to simulate every aspect of a fight, the model learns statistical relationships from historical fighter performance and produces a probability-based prediction.

The prediction engine serves as the foundation upon which the remaining analytical modules are built.

While the prediction model determines **who is likely to win**, the surrounding analytical engines explain **why**.

---

## Prediction Objective

The supervised learning problem is formulated as a binary classification task.

**Input**

A feature vector describing Fighter A and Fighter B.

↓

**Output**

The predicted winner of the matchup.

↓

**Confidence**

The probability associated with that prediction.

---

## Model Selection

Kombat AI uses a **Random Forest Classifier**.

### Why Random Forest?

Several machine learning algorithms were considered during development.

Random Forest was selected because it offers an excellent balance between predictive performance, robustness, and interpretability.

Advantages include:

- Handles non-linear relationships effectively.
- Resistant to overfitting through ensemble learning.
- Performs well on medium-sized structured datasets.
- Naturally estimates prediction probabilities.
- Works without extensive feature scaling.
- Provides feature importance measurements.

These characteristics make Random Forest particularly suitable for combat sports prediction, where relationships between variables are often highly non-linear.

---

## Training Dataset

The prediction model was trained using historical UFC fighter statistics.

Each observation represents a fighter and includes performance metrics describing offensive output, defensive ability, wrestling effectiveness, and grappling efficiency.

The target variable represents fight outcome.

---

## Input Features

The final prediction model uses engineered numerical features extracted from the fighter dataset.

Examples include:

- Wins
- Losses
- Significant Strikes Landed per Minute (SLpM)
- Significant Strikes Absorbed per Minute (SApM)
- Striking Accuracy
- Strike Defence
- Takedown Average
- Takedown Accuracy
- Takedown Defence
- Submission Average
- Reach

These features were selected because they capture the primary statistical characteristics influencing MMA performance.

The exact feature order is stored separately inside:


models/kombat_ai_rf_v2_features.pkl


This guarantees that inference always matches the feature ordering used during training.

---

## Feature Engineering

Raw UFC statistics alone are not sufficient for tactical analysis.

Although the prediction model operates on structured numerical inputs, the application derives additional combat attributes for downstream analytical modules.

Examples include:

- Power
- Durability
- Fight IQ
- Wrestling
- Grappling
- Cardio

These derived attributes are **not** directly learned by the machine learning model.

Instead, they are deterministic calculations built from the original statistical features and are documented separately within the Fight Engine section.

---

## Data Preparation

Before model training, the dataset undergoes preprocessing.

Steps include:

- Handling missing values.
- Converting percentage values into numerical representations.
- Selecting relevant predictive features.
- Removing unnecessary metadata.
- Preparing feature matrices for supervised learning.

The preprocessing pipeline ensures that training and inference remain consistent.

---

## Model Training

The processed dataset is supplied to a Random Forest classifier.

The model learns relationships between fighter statistics and historical fight outcomes through an ensemble of decision trees.

Each tree independently predicts an outcome.

The final prediction is determined by majority voting across all trees within the forest.

This ensemble approach significantly improves robustness compared with a single decision tree.

---

## Model Persistence

After training, the model is exported for inference.

Saved files include:


models/
│
├── kombat_ai_rf_v2.pkl
│
└── kombat_ai_rf_v2_features.pkl


### Model File

Contains the trained Random Forest classifier.

### Feature File

Stores the exact feature ordering expected by the trained model.

Keeping these files separate prevents feature ordering errors during deployment.

---

## Inference Pipeline

During prediction, the following workflow is executed.


Fighter Statistics

↓

Feature Selection

↓

Feature Ordering

↓

Random Forest Model

↓

Prediction Probability

↓

Predicted Winner


The prediction probability is forwarded to additional analytical engines that generate explanations, confidence estimates, tactical recommendations, and visualisations.

---

## Prediction Output

The prediction engine returns:

- Predicted Winner
- Prediction Probability

Example:


Winner:
Islam Makhachev

Win Probability:
78.4%


No tactical reasoning is generated by the prediction engine itself.

Interpretation is delegated to downstream modules.

---

## Integration with the Platform

The prediction engine acts as the first stage of the overall analytical pipeline.


Random Forest Prediction

↓

Confidence Engine

↓

Fight Engine

↓

Recommendation Engine

↓

Explainability Engine

↓

Visualisation Modules

↓

AI Coach


This layered architecture separates prediction from interpretation, making the platform significantly more modular and maintainable.

---

## Current Limitations

The current prediction model operates exclusively on structured statistical data.

It does not directly account for:

- Fighter injuries
- Age-related decline
- Weight-cut quality
- Recent camp changes
- Coaching changes
- Psychological factors
- Short-notice replacements

These contextual factors are instead discussed qualitatively by the AI Coach where relevant.

Future versions may incorporate these variables into the predictive model.

# 5. Main Application (`app.py`)

## Overview

The `app.py` file serves as the entry point of Kombat AI and acts as the central orchestrator for the application's analytical pipeline.

Rather than performing complex calculations itself, the application coordinates communication between multiple independent analytical engines and presents their outputs through an interactive Streamlit interface.

Its primary responsibilities include:

- Initialising the application.
- Loading the AI prediction system.
- Accepting user input.
- Triggering the prediction workflow.
- Displaying analytical visualisations.
- Presenting tactical explanations and recommendations.

---

# 5.1 Application Initialisation

Upon launch, the application performs several setup operations before any user interaction occurs.

### Step 1 — Import Dependencies

The application imports the required libraries for:

- Streamlit interface
- Data manipulation
- Visualisation
- Prediction engine
- Radar visualisation
- Local project modules

These imports establish the environment required for the remainder of the application.

---

### Step 2 — Configure Module Paths

Because the analytical engines are stored inside the `src/` directory, the application dynamically appends the project source directory to Python's import path.

This allows every analytical component to be imported regardless of deployment environment.

---

### Step 3 — Load Cached Resources

The application initialises the `KombatAdvisor` using Streamlit's resource caching mechanism.

python
@st.cache_resource


### Purpose

Loading the machine learning model repeatedly would introduce unnecessary overhead.

Caching ensures that:

- the Random Forest model is loaded only once,
- fighter datasets are reused,
- application responsiveness remains consistent throughout a session.

---

# 5.2 User Interface

The user interface is implemented using Streamlit.

The interface follows a simple analytical workflow requiring minimal user interaction.

Users only need to:

1. Select Fighter One.
2. Select Fighter Two.
3. Press **Predict Fight**.

The remaining analysis is generated automatically.

---

## User Flow


Application Opens

↓

Load Prediction System

↓

User selects Fighter One

↓

User selects Fighter Two

↓

User presses Predict

↓

Generate Full Fight Analysis

↓

Render Visualisations

↓

Display Tactical Report


---

# 5.3 Prediction Workflow

The application follows a sequential analytical pipeline.

Each stage receives outputs from the previous stage before generating additional insights.


Fighter Selection

↓

KombatAdvisor

↓

Prediction Engine

↓

Fight Engine

↓

Confidence Engine

↓

Recommendation Engine

↓

Explainability Engine

↓

Radar Generator

↓

Momentum Simulation

↓

Visual Interface


This pipeline ensures that each analytical component remains independent while contributing to the overall fight report.

---

# 5.4 KombatAdvisor

## Purpose

The `KombatAdvisor` acts as the application's central controller.

Instead of allowing the Streamlit interface to communicate directly with every analytical module, all requests pass through the advisor.

This significantly reduces coupling between interface code and analytical logic.

---

## Responsibilities

The advisor coordinates:

- Fighter retrieval
- Machine learning prediction
- Confidence estimation
- Fight simulation
- Tactical recommendations
- Explainability
- Radar generation
- Momentum generation

By centralising communication, each analytical engine remains modular and reusable.

---

## Internal Workflow


Receive Fighters

↓

Retrieve Fighter Statistics

↓

Generate Prediction

↓

Calculate Confidence

↓

Generate Tactical Analysis

↓

Generate Recommendations

↓

Generate Visualisations

↓

Return Complete Analysis


---

# 5.5 Fighter Selection

Fighters are retrieved from the `FighterRepository`.

The repository loads fighter information from local datasets and returns a searchable list of available fighters.

Using a repository layer rather than directly reading datasets improves maintainability and avoids duplicated data access logic throughout the application.

---

# 5.6 Prediction Request

Once both fighters have been selected, the application constructs a prediction request.

This request contains:

- Fighter One
- Fighter Two

The request is forwarded directly to the `KombatAdvisor`.

The application itself performs no statistical calculations.

---

# 5.7 Fight Analysis Generation

The advisor invokes each analytical subsystem sequentially.

The prediction process includes:

### Prediction Engine

Predicts the likely winner using the Random Forest classifier.

Outputs:

- Winner
- Probability

---

### Fight Engine

Transforms raw fighter statistics into higher-level combat attributes.

Outputs:

- Power
- Accuracy
- Durability
- Wrestling
- Grappling
- Cardio
- Fight IQ

---

### Confidence Engine

Calculates the reliability of the prediction.

Outputs:

- Confidence Score

---

### Recommendation Engine

Generates strategic recommendations for both fighters.

Outputs include:

- Optimal game plans
- Tactical advantages
- Suggested fighting strategies

---

### Explainability Engine

Produces human-readable explanations describing:

- Strengths
- Weaknesses
- Tactical observations
- Matchup reasoning

---

### Radar Engine

Generates radar visualisations using the derived combat attributes.

---

### Momentum Engine

Simulates the evolution of the fight over five rounds.

Outputs:

- Stand-up momentum
- Ground control momentum

---

# 5.8 Rendering Results

Once all analytical engines complete execution, the application renders the final fight report.

The report includes:

- Predicted Winner
- Win Probability
- Confidence Score
- Fighter Radar Chart
- Attribute Comparison
- Momentum Charts
- Tactical Recommendations
- Explainability Report

Each section is generated independently before being combined into a single analytical dashboard.

---

# 5.9 Design Principles

The main application intentionally contains very little analytical logic.

Instead, its primary role is orchestration.

This design offers several advantages:

- Separation of concerns.
- Easier debugging.
- Improved scalability.
- Independent module testing.
- Simplified future expansion.

As a result, new analytical engines can be integrated into Kombat AI without requiring significant modifications to the user interface.

# 6. Fight Engine

## Overview

The Fight Engine is the analytical core of Kombat AI.

While the Prediction Engine determines the most probable winner using machine learning, the Fight Engine transforms raw fighter statistics into interpretable combat attributes that represent real-world fighting capabilities.

These derived attributes are subsequently used throughout the application to power:

- Fighter Radar Charts
- Attribute Comparison
- Momentum Simulation
- Tactical Recommendations
- Explainability Reports
- AI Coaching Context

Unlike the Prediction Engine, which is entirely data-driven, the Fight Engine combines statistical data with combat-specific engineering assumptions to create a more intuitive representation of fighter performance.

---

# 6.1 Attribute Generation

## Purpose

Raw UFC statistics are often difficult for casual users to interpret.

For example, knowing that a fighter lands **5.72 significant strikes per minute** provides little intuitive understanding of their offensive capability.

The Fight Engine converts these raw statistics into higher-level combat attributes scaled between **0 and 100**, making comparisons significantly easier while preserving the relative strengths and weaknesses of each fighter.

---

## Attribute Pipeline


Raw UFC Statistics

↓

Normalisation

↓

Derived Combat Attributes

↓

Radar Charts

Attribute Comparison

Momentum Engine

Explainability Engine

Recommendation Engine


Each attribute is calculated independently before being combined by downstream analytical modules.

---

# 6.2 Power

## Purpose

Power estimates a fighter's offensive striking potential.

Rather than measuring knockout power directly, the attribute measures sustained offensive striking output.

---

## Formula

python
Power = min(100, SLpM × 18)


---

## Inputs

| Variable | Description |
|----------|-------------|
| SLpM | Significant Strikes Landed per Minute |

---

## Why this formula?

Significant Strikes Landed per Minute is one of the strongest publicly available indicators of offensive striking activity.

A fighter consistently landing more strikes generally creates greater damage opportunities over the course of a fight.

---

## Why multiply by 18?

The multiplier converts UFC striking statistics into a combat rating that comfortably fits a 0–100 scale while preserving meaningful separation between elite and average strikers.

Without scaling, the radar visualisations would exhibit minimal differentiation between fighters.

---

## Limitations

Power reflects offensive output rather than finishing ability.

A fighter capable of producing one-shot knockouts despite lower striking volume may receive a lower score than their actual danger would suggest.

---

# 6.3 Accuracy

## Purpose

Measures striking efficiency.

Higher values indicate that a fighter lands a larger percentage of attempted strikes.

---

## Formula

python
Accuracy = Striking Accuracy


---

## Inputs

| Variable | Description |
|----------|-------------|
| Striking Accuracy | Official UFC striking accuracy (%) |

---

## Why this formula?

The UFC already reports striking accuracy as a percentage.

Since the statistic naturally falls within a 0–100 range, no additional transformation is required.

---

## Limitations

Accuracy does not account for:

- strike quality
- damage inflicted
- opponent calibre
- strike selection

---

# 6.4 Durability

## Purpose

Durability estimates a fighter's defensive resilience.

Rather than representing physical toughness alone, this metric combines defensive efficiency with striking absorption.

---

## Formula

python
Durability =
Strike Defence × 0.55 +
(100 − SApM × 8) × 0.45


---

## Inputs

| Variable | Description |
|----------|-------------|
| Strike Defence | Percentage of strikes successfully defended |
| SApM | Significant Strikes Absorbed per Minute |

---

## Why this formula?

Strike Defence represents active defensive skill.

SApM reflects the practical outcome of that defence.

Combining both creates a more balanced representation of survivability.

---

## Why these weights?

Strike Defence receives greater weighting because avoiding strikes generally contributes more to long-term durability than merely absorbing fewer strikes through reduced fight pace.

---

## Limitations

Durability does not directly measure:

- chin strength
- recovery ability
- knockdown resistance
- damage accumulation

---

# 6.5 Wrestling

## Purpose

Represents offensive wrestling effectiveness.

---

## Formula

python
Wrestling =
min(
100,
TD Average × 15 +
TD Accuracy × 0.60
)


---

## Inputs

| Variable | Description |
|----------|-------------|
| TD Average | Average takedowns landed per 15 minutes |
| TD Accuracy | Percentage of successful takedowns |

---

## Why this formula?

Successful wrestling depends on both:

- takedown frequency
- takedown efficiency

Rewarding only volume would overvalue fighters with poor success rates.

Rewarding only accuracy would undervalue high-output wrestlers.

---

## Limitations

This attribute evaluates offensive wrestling only.

Defensive wrestling is incorporated elsewhere.

---

# 6.6 Grappling

## Purpose

Represents offensive submission threat.

---

## Formula

python
Grappling =
min(
100,
Submission Average × 35
)


---

## Inputs

| Variable | Description |
|----------|-------------|
| Submission Average | Submission attempts per 15 minutes |

---

## Why this formula?

Submission attempts provide the strongest publicly available proxy for offensive grappling pressure.

---

## Limitations

The metric does not evaluate:

- positional dominance
- guard retention
- scrambling ability
- defensive grappling

---

# 6.7 Cardio

## Purpose

Estimates a fighter's endurance.

---

## Formula

python
Cardio =
min(
100,
(
(Wins + Losses) × 2.5 +
Strike Defence × 0.30
)
)


---

## Inputs

| Variable | Description |
|----------|-------------|
| Wins | Professional victories |
| Losses | Professional defeats |
| Strike Defence | Defensive striking percentage |

---

## Why this formula?

Experience generally correlates with improved conditioning and pacing.

Strike Defence also tends to decline as fatigue increases, making it a useful secondary endurance indicator.

---

## Limitations

Cardio remains a statistical estimate rather than a physiological measurement.

It cannot account for:

- weight cuts
- altitude
- training camp quality
- illness

---

# 6.8 Fight IQ

## Purpose

Fight IQ estimates overall tactical efficiency.

Rather than measuring intelligence directly, it combines multiple offensive and defensive indicators into a composite decision-making score.

---

## Formula

python
Fight IQ =
Accuracy × 0.25 +
Strike Defence × 0.20 +
TD Accuracy × 0.15 +
TD Defence × 0.15 +
SLpM × 3 −
SApM × 2


---

## Inputs

- Striking Accuracy
- Strike Defence
- Takedown Accuracy
- Takedown Defence
- Significant Strikes Landed per Minute
- Significant Strikes Absorbed per Minute

---

## Why this formula?

No individual UFC statistic adequately represents tactical intelligence.

Fight IQ therefore combines several indicators reflecting:

- offensive efficiency
- defensive awareness
- wrestling competence
- striking effectiveness

---

## Why these weights?

Accuracy receives the greatest weighting because efficient offence generally reflects superior decision-making.

Defensive metrics receive substantial emphasis to reward fighters capable of managing risk while maintaining offensive effectiveness.

---

## Limitations

Fight IQ cannot directly quantify:

- adaptability
- strategic adjustments
- corner advice
- mental composure
- fight planning

It should therefore be interpreted as a statistical approximation rather than a psychological measurement.

# 6.9 Stand-up Score

## Purpose

The Stand-up Score estimates a fighter's overall effectiveness during striking exchanges.

Unlike the Power attribute, which measures offensive output alone, the Stand-up Score evaluates striking as a combination of offensive efficiency, defensive capability, and damage sustainability.

This score is primarily used by:

- Momentum Simulation
- Tactical Analysis
- Fight Breakdown
- Recommendation Engine

---

## Calculation Philosophy

Winning striking exchanges depends on significantly more than simply throwing punches.

The Stand-up Score therefore combines multiple aspects of striking performance:

- Offensive output
- Offensive efficiency
- Defensive awareness
- Damage avoidance

By combining these factors, the score attempts to approximate a fighter's overall effectiveness during stand-up exchanges.

---

## Inputs

The calculation considers:

- Significant Strikes Landed per Minute (SLpM)
- Significant Strikes Absorbed per Minute (SApM)
- Striking Accuracy
- Strike Defence

---

## Interpretation

Higher values indicate fighters who:

- Land strikes consistently.
- Absorb relatively little damage.
- Strike efficiently.
- Defend effectively.

Lower values indicate fighters who rely less on striking or who are statistically vulnerable during stand-up exchanges.

---

## Limitations

The Stand-up Score does not directly measure:

- Knockout power
- Footwork
- Counter-striking ability
- Timing
- Distance management

These characteristics remain difficult to quantify using publicly available statistics.

---

# 6.10 Ground Control Score

## Purpose

The Ground Control Score estimates a fighter's effectiveness during grappling exchanges.

Unlike the Wrestling and Grappling attributes, which evaluate individual skills independently, the Ground Control Score combines offensive wrestling with submission ability to estimate complete ground dominance.

---

## Calculation Philosophy

Ground control in mixed martial arts depends upon multiple complementary skills.

The score therefore considers:

- Wrestling
- Submission Threat
- Grappling Pressure

rather than evaluating any single statistic in isolation.

---

## Inputs

Primary inputs include:

- Takedown Average
- Takedown Accuracy
- Submission Average

---

## Interpretation

Higher values indicate fighters capable of:

- Securing takedowns consistently.
- Maintaining positional control.
- Creating submission opportunities.

---

## Limitations

The Ground Control Score does not explicitly measure:

- Top control time
- Scrambling ability
- Guard passing
- Positional transitions

These statistics are not consistently available within public UFC datasets.

---

# 6.11 Fighting Style Engine

## Purpose

The Fighting Style Engine assigns a combat archetype to every fighter.

Rather than treating all fighters identically, Kombat AI recognises stylistic differences that influence fight dynamics beyond numerical statistics.

Examples include:

- Pressure Wrestler
- Counter Striker
- Sambo Grappler
- Kickboxer
- Boxer Grappler
- Well Rounded Finisher
- BJJ Specialist
- Chaos Pressure Fighter

---

## Why Styles Matter

Two fighters may possess nearly identical statistical profiles while approaching fights in completely different ways.

For example:

A pressure wrestler continuously attempts to close distance and initiate grappling exchanges.

A counter striker may land fewer strikes overall while producing greater efficiency through defensive timing.

These behavioural differences significantly influence fight momentum and tactical recommendations.

---

## Implementation

Each fighter is assigned a single primary fighting style.

This classification is stored alongside fighter information and is used throughout the application whenever stylistic modifiers are required.

---

## Applications

Fighting styles influence:

- Momentum Simulation
- Tactical Analysis
- AI Coach Responses
- Recommendation Engine

---

## Limitations

The current implementation assumes one dominant fighting style per fighter.

Many elite fighters naturally evolve throughout their careers or adopt different strategies against different opponents.

Future versions may support multiple weighted fighting styles.

---

# 6.12 Momentum Engine

## Purpose

The Momentum Engine simulates how a fight evolves over multiple rounds.

Unlike the Prediction Engine, which produces a single outcome, the Momentum Engine estimates the changing balance of a contest throughout five rounds.

This creates a more realistic representation of fight progression.

---

## Philosophy

Real fights are dynamic.

Momentum constantly shifts due to:

- fatigue
- offensive success
- defensive adjustments
- wrestling pressure
- striking exchanges

The Momentum Engine attempts to model these fluctuations rather than assuming a constant level of performance throughout the contest.

---

## Components

The simulation consists of two independent systems.

### Stand-up Momentum

Represents striking exchanges throughout the fight.

---

### Ground Momentum

Represents grappling and wrestling control throughout the fight.

---

## Inputs

Momentum calculations utilise:

- Stand-up Score
- Ground Control Score
- Cardio
- Fight IQ
- Fighting Style

Each contributes differently to the evolution of momentum.

---

## Simulation Process

For each round:


Previous Momentum

↓

Cardio Adjustment

↓

Style Modifier

↓

Performance Variance

↓

Updated Momentum


This process repeats for all five rounds.

---

## Why Cardio?

Fighters with superior endurance tend to maintain performance levels deeper into fights.

Lower cardio values gradually reduce momentum as rounds progress.

---

## Why Fighting Style?

Certain fighting styles naturally produce different momentum patterns.

For example:

- Pressure wrestlers typically accumulate momentum steadily.
- Counter strikers often experience sharper momentum swings.
- Chaos fighters produce greater volatility.

These modifiers improve realism without introducing unnecessary complexity.

---

## Random Variance

No fight unfolds identically.

The simulation therefore incorporates controlled randomness to reflect:

- successful exchanges
- momentum swings
- unpredictable moments

The variance remains intentionally constrained to prevent unrealistic outcomes.

---

## Outputs

The Momentum Engine produces:

- Stand-up Momentum Curve
- Ground Control Momentum Curve

These curves are visualised throughout the application.

---

## Limitations

The simulation remains statistical rather than physical.

It does not currently account for:

- knockdowns
- injuries
- referee interventions
- corner adjustments
- fight-ending events

Future versions may incorporate event-driven simulations.

# 7. Confidence Engine

## Overview

The Prediction Engine produces a probability for the predicted winner.

However, probability alone does not necessarily represent prediction reliability.

The Confidence Engine converts the model's raw probability into a more interpretable confidence score that is displayed throughout the application.

---

## Purpose

The Confidence Engine exists to answer a simple question:

> **"How confident should the user be in this prediction?"**

Rather than exposing raw machine learning outputs, Kombat AI presents a confidence estimate that is easier for users to understand.

---

## Inputs

The engine primarily evaluates:

- Predicted Probability
- Separation between both fighters
- Overall statistical advantage

---

## Output

Example


Winner
Islam Makhachev

Win Probability
78.4%

Confidence
High


---

## Interpretation

Higher confidence generally indicates:

- Clear statistical superiority.
- Greater separation between fighter profiles.
- Lower prediction uncertainty.

Lower confidence usually represents closely matched contests where both fighters possess comparable statistical profiles.

---

## Design Philosophy

Confidence is intentionally separated from prediction probability.

This distinction allows future versions of Kombat AI to incorporate additional uncertainty measures such as:

- Prediction consistency
- Historical model calibration
- Dataset density
- Out-of-distribution detection

without modifying the Prediction Engine itself.

---

## Limitations

The current confidence score is derived primarily from model outputs.

It does not currently consider:

- unseen stylistic interactions
- late replacement fighters
- injuries
- external contextual information
- betting market disagreement

These remain opportunities for future improvement.

# 8. Explainability Engine

## Overview

Machine learning models frequently provide accurate predictions without explaining the reasoning behind those predictions.

The Explainability Engine bridges this gap by translating numerical outputs into human-readable analytical insights.

---

## Purpose

The Explainability Engine answers the question:

> **"Why did Kombat AI predict this result?"**

Rather than presenting only probabilities, the system generates explanations highlighting the statistical advantages responsible for the prediction.

---

## Inputs

The engine analyses:

- Derived Combat Attributes
- Statistical Differences
- Fighter Strengths
- Fighter Weaknesses
- Momentum Indicators

---

## Output

Typical explanations include observations such as:

- Superior striking efficiency.
- Wrestling advantage.
- Defensive superiority.
- Higher pace.
- Better cardio.
- Greater submission threat.

These explanations are presented as structured tactical insights rather than technical machine learning terminology.

---

## Design Philosophy

Interpretability was prioritised throughout Kombat AI.

The goal was to ensure that every prediction could be accompanied by understandable reasoning rather than functioning as a black-box classifier.

---

## Limitations

The Explainability Engine interprets statistical differences rather than model internals.

It should therefore be viewed as an analytical interpretation of the prediction rather than a formal explanation of the Random Forest decision process.

# 9. Recommendation Engine

## Overview

The Recommendation Engine transforms statistical analysis into actionable tactical advice.

Rather than simply predicting a winner, Kombat AI attempts to answer:

> **"How should each fighter approach this matchup?"**

---

## Purpose

The Recommendation Engine generates strategic recommendations tailored to both fighters.

These recommendations consider:

- striking advantages
- grappling opportunities
- defensive weaknesses
- momentum trends
- fighting styles

---

## Inputs

The engine analyses:

- Combat Attributes
- Fighting Styles
- Momentum Scores
- Stand-up Score
- Ground Control Score

---

## Output

Example recommendations include:

### Fighter A

- Maintain distance.
- Pressure with combinations.
- Avoid prolonged grappling exchanges.

### Fighter B

- Close distance early.
- Initiate wrestling.
- Slow the pace.
- Target positional control.

---

## Design Philosophy

Rather than recommending generic strategies, the engine attempts to identify the statistically optimal game plan based on the matchup itself.

This produces more personalised analytical reports.

---

## Limitations

Recommendations are generated using deterministic analytical rules rather than reinforcement learning or fight simulation.

Consequently, they should be interpreted as statistically informed tactical suggestions rather than guaranteed winning strategies.

# 10. What If Lab

## Overview

The What If Lab is an interactive simulation environment that allows users to create hypothetical fight scenarios by modifying fighter attributes before generating a completely new prediction.

Unlike the main prediction page, which analyses fighters using their official statistics, the What If Lab enables users to answer questions such as:

- What if Fighter A had better cardio?
- What if Fighter B became a better wrestler?
- What if both fighters were equally durable?
- What if one fighter improved their striking accuracy?

Every modification immediately influences the prediction pipeline, allowing users to observe how individual attributes affect fight outcomes.

---

# 10.1 Purpose

The purpose of the What If Lab is to demonstrate how different combat attributes contribute to prediction outcomes.

Rather than functioning as a fantasy game, it serves as an educational analytical tool that helps users understand the relative importance of different fighting skills.

---

# 10.2 Workflow

The simulation follows the pipeline below.


Select Fighter One

↓

Select Fighter Two

↓

Load Official Statistics

↓

Modify Fighter Attributes

↓

Generate Updated Prediction

↓

Calculate Confidence

↓

Generate Tactical Explanation

↓

Generate AI Commentary

↓

Display New Result


Unlike the main application, the fighter statistics are no longer treated as immutable.

Instead, temporary modified profiles are created for simulation purposes.

---

# 10.3 Attribute Modification

Each fighter's statistical profile can be adjusted independently.

The modified profile exists only during the current simulation and does not overwrite the original dataset.

Typical adjustable attributes include:

- Power
- Accuracy
- Durability
- Wrestling
- Grappling
- Cardio
- Fight IQ

These adjustments simulate improvements or declines in fighter performance.

---

# 10.4 Temporary Fighter Profiles

Instead of editing the original fighter records, the application creates temporary copies.

Conceptually:


Official Fighter Profile

↓

Deep Copy

↓

Apply User Changes

↓

Run Prediction

↓

Discard Modified Copy


This guarantees that:

- Original data remains unchanged.
- Multiple simulations can be performed safely.
- Every simulation begins from official fighter statistics.

---

# 10.5 Prediction Pipeline

Once the modified profiles are generated, the prediction process becomes identical to the main application.

The What If Lab invokes:

- Prediction Engine
- Fight Engine
- Confidence Engine
- Explainability Engine
- Recommendation Engine
- AI Coach

The only difference is that these engines operate on the modified fighter profiles rather than the official database.

---

# 10.6 Confidence Recalculation

Every attribute adjustment changes the fighter feature vector.

Consequently:

- predicted winner,
- win probability,
- confidence score,

are recalculated from scratch after every simulation.

No previous prediction values are reused.

---

# 10.7 Explainability

Following each simulation, the Explainability Engine generates an updated analytical report describing why the prediction changed.

For example:

Increasing a fighter's wrestling ability may produce explanations such as:

- Improved takedown success.
- Greater ground control.
- Better positional dominance.

These explanations are generated using the modified statistics rather than the official fighter data.

---

# 10.8 AI Coach Integration

The What If Lab integrates directly with the LLM Coach.

After each simulation, the modified fight statistics are supplied as additional context for the language model.

This enables the AI Coach to discuss hypothetical scenarios naturally.

Example questions include:

- Would this version of the fighter defeat the champion?
- Does improving cardio matter more than improving power?
- Which single attribute would produce the greatest improvement?

The AI therefore reasons about the modified matchup rather than the original fighters.

---

# 10.9 Engineering Decisions

Several important design decisions were made during implementation.

## Temporary Simulation

Attribute modifications are never written to disk.

This prevents accidental corruption of the official fighter database.

---

## Modular Pipeline

The What If Lab reuses the same analytical engines used by the main application.

This guarantees consistency between official predictions and hypothetical simulations while avoiding duplicate code.

---

## Independent Recalculation

Every simulation executes a completely new prediction pipeline.

No intermediate analytical results are cached after attribute modification.

Although this introduces a slight computational overhead, it ensures analytical correctness.

---

# 10.10 Limitations

The current implementation modifies statistical attributes only.

It does not currently simulate:

- age progression,
- weight class changes,
- stylistic evolution,
- injuries,
- coaching improvements,
- psychological factors,
- training camp quality.

These remain potential extensions for future versions of Kombat AI.

# 11. AI Coach

## Overview

The AI Coach is an interactive conversational assistant designed to answer user questions about UFC fighters, fight matchups, tactical strategies, and hypothetical scenarios.

Unlike traditional chatbots that rely entirely on a large language model, the AI Coach combines structured statistical analysis with Retrieval-Augmented Generation (RAG) and persistent conversation memory.

This architecture enables the assistant to provide responses that are grounded in factual fighter data while maintaining conversational continuity.

---

# 11.1 Objectives

The AI Coach was designed with four primary objectives:

- Provide statistically grounded responses.
- Explain fight predictions in natural language.
- Maintain conversational context.
- Support hypothetical reasoning generated inside the What If Lab.

---

# 11.2 System Architecture

The AI Coach combines several independent modules.


User Question

↓

Memory Engine

↓

Retriever

↓

Knowledge Base

↓

Prompt Builder

↓

Gemini LLM

↓

Response


Each module performs a specialised task before passing information to the next stage.

---

# 11.3 Retrieval-Augmented Generation (RAG)

## Purpose

Large Language Models frequently hallucinate when asked about niche sporting statistics.

To reduce hallucinations, Kombat AI employs Retrieval-Augmented Generation (RAG).

Rather than asking Gemini to answer from its own knowledge, the system first retrieves relevant fighter information from the local knowledge base.

Only this retrieved information is supplied as context to the language model.

---

## Workflow


User Query

↓

Vector Retrieval

↓

Relevant Fighter Documents

↓

Prompt Construction

↓

Gemini Response


This ensures that responses remain grounded in the application's fighter database rather than relying on external model memory.

---

# 11.4 Fighter Knowledge Base

The knowledge base consists of structured fighter information generated during preprocessing.

Each fighter document contains information such as:

- Personal details
- Professional record
- Striking statistics
- Wrestling statistics
- Grappling statistics
- Derived combat attributes
- Fighting style

These documents form the factual foundation used by the retrieval system.

---

# 11.5 Retriever

## Purpose

The Retriever identifies which fighter documents are most relevant to the user's question.

Rather than loading every fighter profile into the language model context, only the most relevant documents are selected.

This improves both efficiency and factual consistency.

---

## Retrieval Process


User Question

↓

Sentence Embedding

↓

Vector Similarity Search

↓

Top Matching Documents

↓

Prompt Builder


---

## Advantages

Using retrieval offers several benefits:

- Reduced hallucination.
- Lower prompt size.
- Faster responses.
- Improved factual grounding.

---

# 11.6 Prompt Engineering

The retrieved fighter information is incorporated into a carefully designed system prompt before being sent to Gemini.

The prompt instructs the model to:

- Answer using retrieved information whenever possible.
- Avoid inventing statistics.
- Explain reasoning clearly.
- Maintain an analytical tone.
- Provide tactical insight rather than generic commentary.

Prompt engineering ensures that the language model behaves consistently across different types of questions.

---

# 11.7 Conversation Memory

## Purpose

The Memory Engine stores previous interactions during a conversation.

Instead of treating every message independently, the AI Coach remembers earlier exchanges.

For example:

User:


How would Islam beat Charles?


Later:


What if Charles improved his wrestling?


The second question can be interpreted correctly because the assistant remembers the previous discussion.

---

## Workflow


User Message

↓

Conversation History

↓

Prompt Builder

↓

Gemini

↓

Updated Memory


---

## Advantages

Persistent memory enables:

- Follow-up questions.
- Natural conversation.
- Reduced repetition.
- Better contextual reasoning.

---

# 11.8 Gemini Integration

The language model responsible for response generation is Google's Gemini API.

The AI Coach does not directly expose Gemini to the user.

Instead, Gemini receives:

- Retrieved fighter documents.
- Previous conversation.
- System instructions.
- Current user query.

Gemini therefore acts as the reasoning engine rather than the information source.

---

# 11.9 AI Coach Workflow

Complete pipeline:


User Question

↓

Memory Engine

↓

Retriever

↓

Knowledge Base

↓

Prompt Builder

↓

Gemini

↓

Response

↓

Conversation Memory Updated


---

# 11.10 Design Decisions

Several architectural decisions were made during implementation.

## Local Knowledge First

The AI always attempts to answer using retrieved fighter information before relying on the language model's internal knowledge.

This significantly reduces hallucination.

---

## Modular Design

The AI Coach separates:

- retrieval,
- prompting,
- memory,
- language model,

into independent modules.

Each can therefore be replaced without affecting the remaining pipeline.

---

## Memory Isolation

Conversation memory is stored separately from fighter knowledge.

This prevents user conversations from contaminating factual fighter information.

---

# 11.11 Limitations

The AI Coach currently depends upon:

- locally stored fighter documents,
- Gemini API availability,
- prompt engineering.

It does not currently support:

- live UFC event updates,
- internet search,
- real-time rankings,
- automatic fighter database updates.

Future versions may integrate external APIs for continuously updated information.

# 12. Deployment

## Overview

Kombat AI was designed to be lightweight, reproducible, and easily deployable using modern cloud-hosted tooling.

The project follows a modular architecture that separates the user interface, analytical engines, datasets, and machine learning models, allowing the application to run consistently across both local development and cloud deployment.

---

# 12.1 Local Development Environment

The application was developed using Python inside an isolated virtual environment.

Core development tools included:

- Python 3
- Git
- GitHub
- VS Code
- Streamlit
- Pandas
- Scikit-learn
- Sentence Transformers
- Google Gemini API

All required dependencies are listed inside `requirements.txt`, allowing the complete environment to be recreated with a single installation command.

---

# 12.2 Project Structure

The project follows a modular directory structure.


kombat-ai/

│

├── app/

│   ├── app.py

│   └── pages/

│

├── src/

│

├── data/

│

├── models/

│

├── docs/

│

├── requirements.txt

│

└── README.md


Each directory has a clearly defined responsibility.

| Directory | Purpose |
|------------|----------|
| app | Streamlit interface |
| src | Core analytical engines |
| data | Fighter datasets |
| models | Trained ML models |
| docs | Technical documentation |

---

# 12.3 Version Control

Git was used throughout development.

Version control was employed for:

- feature development
- experimentation
- bug fixing
- deployment management

The project utilised multiple branches before merging features into the production branch.

---

# 12.4 GitHub Repository

The complete project is hosted publicly on GitHub.

GitHub serves as:

- source code repository
- version history
- collaboration platform
- deployment source for Streamlit Cloud

---

# 12.5 Streamlit Cloud Deployment

The production application is deployed using Streamlit Community Cloud.

Deployment process:


GitHub Repository

↓

Streamlit Cloud

↓

Automatic Build

↓

requirements.txt Installation

↓

Application Launch


The application automatically rebuilds whenever new commits are pushed to the main branch.

---

# 12.6 Environment Variables

Certain application features require secure API credentials.

Sensitive information is therefore stored using Streamlit Secrets rather than being committed to Git.

Example:


GEMINI_API_KEY = ********


This approach ensures:

- API keys remain private.
- Public repository remains secure.
- Cloud deployment functions correctly.

---

# 12.7 Deployment Challenges

Several deployment issues were encountered during development.

### Module Imports

Relative imports functioned locally but initially failed on Streamlit Cloud.

The import structure was standardised to use package-level imports throughout the project.

---

### Missing Datasets

CSV datasets were originally ignored by `.gitignore`, causing deployment failures.

Required datasets were explicitly tracked and committed for deployment.

---

### Missing Machine Learning Models

The trained Random Forest model was excluded from version control.

The model files were later force-added to ensure successful deployment.

---

### API Configuration

Gemini integration initially failed because the deployment environment lacked the required API key.

The issue was resolved using Streamlit Secrets.

---

# 12.8 Current Deployment Status

The deployed application currently supports:

- Fight Prediction
- Fighter Comparison
- What If Lab
- AI Coach
- Interactive Radar Charts
- Tactical Analysis
- Recommendation Engine

The deployment mirrors the local development version.

# 13. Engineering Decisions

## Overview

Throughout development, several architectural decisions were made to balance realism, maintainability, interpretability, and deployment simplicity.

Rather than pursuing maximum model complexity, Kombat AI prioritises transparency and modularity.

---

# 13.1 Why Random Forest?

Several algorithms were considered during development.

The final prediction model uses a Random Forest classifier.

### Reasons

- Strong performance on structured tabular data.
- Naturally handles nonlinear relationships.
- Requires minimal feature scaling.
- Resistant to overfitting compared to single decision trees.
- Produces stable probability estimates.

Random Forest also offered excellent performance while remaining lightweight enough for real-time predictions inside Streamlit.

---

# 13.2 Why Derived Combat Attributes?

Raw UFC statistics are difficult for users to interpret.

Instead of exposing dozens of isolated statistics, Kombat AI derives higher-level combat attributes such as:

- Power
- Wrestling
- Grappling
- Cardio
- Fight IQ

These attributes improve interpretability while also supporting downstream analytical modules.

---

# 13.3 Why Modular Architecture?

Every major subsystem was implemented independently.

Examples include:

- Prediction Engine
- Fight Engine
- Momentum Engine
- Recommendation Engine
- Confidence Engine
- Explainability Engine
- AI Coach

This separation offers several advantages.

- Easier debugging.
- Improved maintainability.
- Independent testing.
- Simplified future upgrades.

---

# 13.4 Why Retrieval-Augmented Generation?

A traditional LLM often hallucinates when discussing niche sporting statistics.

To reduce hallucination, Kombat AI retrieves relevant fighter information before constructing prompts for Gemini.

Benefits include:

- improved factual accuracy
- reduced hallucination
- smaller prompts
- better reproducibility

---

# 13.5 Why Local Datasets?

Instead of relying on live UFC APIs, the application currently operates using curated local datasets.

Reasons include:

- reproducibility
- consistent preprocessing
- faster inference
- simplified deployment
- independence from third-party services

---

# 13.6 Why Streamlit?

Several frontend technologies were evaluated.

Streamlit was selected because it provides:

- rapid prototyping
- interactive visualisations
- Python-native development
- simple cloud deployment
- minimal frontend complexity

This allowed development effort to focus primarily on analytical functionality.

---

# 13.7 Why Temporary Simulations?

The What If Lab creates temporary fighter profiles instead of modifying the official dataset.

This guarantees:

- data integrity
- reproducible simulations
- safe experimentation
- consistent official statistics

---

# 13.8 Why Momentum Simulation?

Traditional prediction models provide only a winner.

Real fights evolve dynamically.

The Momentum Engine was introduced to simulate changing fight dynamics throughout multiple rounds, making predictions more engaging and easier to interpret.

---

# 13.9 Engineering Trade-offs

Several conscious trade-offs were accepted during development.

| Decision | Benefit | Limitation |
|----------|----------|------------|
| Local datasets | Fast, reproducible | No live updates |
| Random Forest | Stable, interpretable | Less expressive than deep learning |
| Rule-based recommendations | Explainable | Less adaptive |
| Single fighting style | Simpler implementation | Less realistic for hybrid fighters |
| Statistical simulation | Fast inference | Not physics-based |

These trade-offs prioritised reliability and maintainability over unnecessary complexity.

# 14. Future Improvements

Although Kombat AI is fully functional, several opportunities remain for future development.

---

# 14.1 Machine Learning

Potential improvements include:

- Gradient Boosting models.
- XGBoost comparison.
- Ensemble learning.
- Probability calibration.
- SHAP explainability.
- Automated retraining pipeline.

---

# 14.2 Data

Future datasets could include:

- Live UFC statistics.
- Official rankings.
- Fight camp information.
- Injury reports.
- Weight cut history.
- Championship statistics.
- Round-by-round data.

---

# 14.3 Artificial Intelligence

The AI Coach can be expanded using modern agentic architectures.

Possible improvements include:

- Multi-agent reasoning.
- Tool calling.
- Internet search integration.
- Better long-term memory.
- Retrieval optimisation.
- Context-aware tactical planning.

---

# 14.4 Product Features

Potential user-facing improvements include:

- User accounts.
- Saved simulations.
- Prediction history.
- Fantasy tournaments.
- Community leaderboards.
- Favourite fighters.
- Personal dashboards.

---

# 14.5 Visualisation

Future visual improvements include:

- Animated momentum timelines.
- Interactive fight maps.
- Expanded radar comparisons.
- Round-by-round analytics.
- Heat-map visualisations.
- Tactical replay dashboards.

---

# 14.6 Infrastructure

Future deployment improvements include:

- Docker containerisation.
- CI/CD pipelines.
- Automated testing.
- Cloud-hosted databases.
- Model versioning.
- Centralised logging.
- Monitoring dashboards.

---

# 14.7 Long-Term Vision

The long-term objective is to transform Kombat AI from a prediction platform into a comprehensive combat sports intelligence system capable of providing:

- Statistical analysis.
- Tactical coaching.
- Fantasy simulations.
- Interactive AI conversations.
- Live event support.
- Advanced explainability.
- Educational combat analytics.

Ultimately, Kombat AI aims to demonstrate how machine learning, data science, retrieval systems, and modern large language models can be integrated into a single intelligent analytical platform for combat sports.