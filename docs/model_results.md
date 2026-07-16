# Kombat AI V1 — Model Results

## Dataset
- Original cleaned dataset: 7,930 UFC fights
- Balanced training data created by mirroring fighter corners
- Only pre-fight statistics were used

## Model
- Random Forest Classifier
- 300 decision trees
- Random state: 42

## Data Preparation
- Removed tournament and unsupported division categories
- Converted interim divisions to their standard divisions
- Filled missing reach, height, and weight values using medians
- Excluded fight statistics that would cause target leakage
- Addressed red-corner bias by mirroring each fight
- Split original fights before mirroring to prevent train-test leakage

## Final Evaluation
- Leakage-safe accuracy: 70.37%
- Class 0 precision: 70%
- Class 0 recall: 71%
- Class 0 F1-score: 70%
- Class 1 precision: 71%
- Class 1 recall: 70%
- Class 1 F1-score: 70%

## Earlier Experiments
- Original unbalanced Random Forest accuracy: 72.01%
- Difference-only feature model accuracy: 70.49%
- Randomly split mirrored dataset accuracy: 70.43%

## Final Model File
`models/kombat_ai_rf.pkl`

## Conclusion
The final model provides balanced predictions for both fighter positions and achieves approximately 70% accuracy without using post-fight information or leaking mirrored copies across the train-test split.