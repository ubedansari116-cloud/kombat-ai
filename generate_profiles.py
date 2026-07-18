import pandas as pd
import os

# Target directory matching your project's docs folder
target_dir = "docs"
os.makedirs(target_dir, exist_ok=True)

# Load the fighter stats from your data directory
csv_path = "data/ufc-fighters-statistics.csv"

if not os.path.exists(csv_path):
    print(f"Error: Could not find {csv_path}. Double-check your path.")
    exit()

df = pd.read_csv(csv_path)

# Generate a clean text file per fighter
for _, row in df.iterrows():
    name = str(row.get('name', '')).strip()
    if not name or name.lower() == 'nan':
        continue
        
    filename = f"{name.lower().replace(' ', '_')}.txt"
    filepath = os.path.join(target_dir, filename)
    
    profile_text = f"""Fighter Profile: {name}
Nickname: {row.get('nickname', 'N/A')}
Record: {row.get('wins', 0)} W - {row.get('losses', 0)} L - {row.get('draws', 0)} D
Height: {row.get('height', 'N/A')}
Weight: {row.get('weight', 'N/A')} lbs
Reach: {row.get('reach', 'N/A')}
Stance: {row.get('stance', 'N/A')}

Striking Statistics:
- SLpM (Significant Strikes Landed per Min): {row.get('SLpM', 0)}
- Str. Acc. (Striking Accuracy): {row.get('Str_Acc', 0)}%
- SApM (Significant Strikes Absorbed per Min): {row.get('SApM', 0)}
- Str. Def. (Striking Defense): {row.get('Str_Def', 0)}%

Grappling Statistics:
- TD Avg (Average Takedowns per 15 min): {row.get('TD_Avg', 0)}
- TD Acc (Takedown Accuracy): {row.get('TD_Acc', 0)}%
- TD Def (Takedown Defense): {row.get('TD_Def', 0)}%
- Sub Avg (Average Submissions Attempted per 15 min): {row.get('Sub_Avg', 0)}
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(profile_text.strip())

print(f"Successfully generated text profiles for {len(df)} fighters in '{target_dir}/'.")
