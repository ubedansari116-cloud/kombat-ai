#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data")


# In[3]:


fighters_primary = pd.read_csv(DATA_DIR / "fighter_details.csv")
fighters_secondary = pd.read_csv(DATA_DIR / "ufc-fighters-statistics.csv")
fights = pd.read_csv(DATA_DIR / "fight_details.csv")
events = pd.read_csv(DATA_DIR / "event_details.csv")
ufc = pd.read_csv(DATA_DIR / "UFC.csv")


# In[4]:


print("fighters_primary:", fighters_primary.shape)
print("fighters_secondary:", fighters_secondary.shape)
print("fights:", fights.shape)
print("events:", events.shape)
print("ufc:", ufc.shape)


# In[5]:


for name, df in {
    "fighters_primary": fighters_primary,
    "fighters_secondary": fighters_secondary,
    "fights": fights,
    "events": events,
    "ufc": ufc,
}.items():
    print(f"\n{name.upper()}")
    print(df.columns.tolist())


# In[6]:


ufc.columns.tolist()


# In[7]:


ufc.head(3)


# In[8]:


audit = pd.DataFrame({
    "dtype": ufc.dtypes.astype(str),
    "missing_count": ufc.isna().sum(),
    "missing_percent": (ufc.isna().mean() * 100).round(2),
    "unique_values": ufc.nunique()
}).sort_values("missing_percent", ascending=False)

audit.head(30)


# In[9]:


ufc["winner"].value_counts(dropna=False)


# In[10]:


ufc["winner"].head(20).tolist()


# In[11]:


ufc[["winner", "r_name", "b_name"]].head(10)


# In[12]:


ufc = ufc.dropna(subset=["winner"]).copy()

ufc["target"] = (ufc["winner"] == ufc["r_name"]).astype(int)

ufc["target"].value_counts()


# In[13]:


ufc["target"].value_counts(normalize=True) * 100


# In[14]:


features = [
    "r_wins",
    "r_losses",
    "r_height",
    "r_weight",
    "r_reach",
    "r_splm",
    "r_str_acc",
    "r_sapm",
    "r_str_def",
    "r_td_avg",
    "r_td_avg_acc",
    "r_td_def",
    "r_sub_avg",

    "b_wins",
    "b_losses",
    "b_height",
    "b_weight",
    "b_reach",
    "b_splm",
    "b_str_acc",
    "b_sapm",
    "b_str_def",
    "b_td_avg",
    "b_td_avg_acc",
    "b_td_def",
    "b_sub_avg",

    "division",
    "title_fight"
]

ml_df = ufc[features + ["target"]].copy()

ml_df.shape


# In[15]:


ml_df.isna().sum().sort_values(ascending=False)


# In[16]:


ml_df.dtypes


# In[17]:


df = ml_df.copy()

# Reach / size
df["height_diff"] = df["r_height"] - df["b_height"]
df["weight_diff"] = df["r_weight"] - df["b_weight"]
df["reach_diff"] = df["r_reach"] - df["b_reach"]

# Experience
df["wins_diff"] = df["r_wins"] - df["b_wins"]
df["losses_diff"] = df["r_losses"] - df["b_losses"]

# Striking
df["splm_diff"] = df["r_splm"] - df["b_splm"]
df["str_acc_diff"] = df["r_str_acc"] - df["b_str_acc"]
df["sapm_diff"] = df["r_sapm"] - df["b_sapm"]
df["str_def_diff"] = df["r_str_def"] - df["b_str_def"]

# Wrestling
df["td_avg_diff"] = df["r_td_avg"] - df["b_td_avg"]
df["td_acc_diff"] = df["r_td_avg_acc"] - df["b_td_avg_acc"]
df["td_def_diff"] = df["r_td_def"] - df["b_td_def"]

# Submission threat
df["sub_avg_diff"] = df["r_sub_avg"] - df["b_sub_avg"]

df.head()


# In[18]:


df["division"].value_counts()


# In[19]:


sorted(df["division"].unique())


# In[20]:


df = ml_df.copy()

df["division"] = df["division"].str.lower()

# Remove interim prefix
df["division"] = df["division"].str.replace("interim ", "", regex=False)

valid_divisions = [
    "flyweight",
    "bantamweight",
    "featherweight",
    "lightweight",
    "welterweight",
    "middleweight",
    "light heavyweight",
    "heavyweight",
    "women's strawweight",
    "women's flyweight",
    "women's bantamweight",
    "women's featherweight"
]

df = df[df["division"].isin(valid_divisions)].copy()

print(df.shape)
print(df["division"].value_counts())


# In[21]:


df.isna().sum().sort_values(ascending=False).head(20)


# In[22]:


# Fill numeric missing values

for col in [
    "r_reach", "b_reach",
    "r_height", "b_height",
    "r_weight", "b_weight"
]:
    df[col] = df[col].fillna(df[col].median())

df.isna().sum().sort_values(ascending=False).head(10)


# In[23]:


df = pd.get_dummies(
    df,
    columns=["division"],
    drop_first=True
)

df.shape


# In[24]:


X = df.drop(columns=["target"])
y = df["target"]

print(X.shape)
print(y.shape)


# In[25]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(X_train.shape)
print(X_test.shape)


# In[26]:


from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)


# In[27]:


from sklearn.metrics import accuracy_score

preds = rf.predict(X_test)

accuracy = accuracy_score(y_test, preds)

print("Accuracy:", accuracy)


# In[28]:


importance = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_
})

importance.sort_values(
    "importance",
    ascending=False
).head(20)


# In[31]:


# Create matchup-difference features

df_v2 = df.copy()

df_v2["wins_diff"] = df_v2["r_wins"] - df_v2["b_wins"]
df_v2["losses_diff"] = df_v2["r_losses"] - df_v2["b_losses"]

df_v2["height_diff"] = df_v2["r_height"] - df_v2["b_height"]
df_v2["weight_diff"] = df_v2["r_weight"] - df_v2["b_weight"]
df_v2["reach_diff"] = df_v2["r_reach"] - df_v2["b_reach"]

df_v2["splm_diff"] = df_v2["r_splm"] - df_v2["b_splm"]
df_v2["str_acc_diff"] = df_v2["r_str_acc"] - df_v2["b_str_acc"]
df_v2["sapm_diff"] = df_v2["r_sapm"] - df_v2["b_sapm"]
df_v2["str_def_diff"] = df_v2["r_str_def"] - df_v2["b_str_def"]

df_v2["td_avg_diff"] = df_v2["r_td_avg"] - df_v2["b_td_avg"]
df_v2["td_acc_diff"] = df_v2["r_td_avg_acc"] - df_v2["b_td_avg_acc"]
df_v2["td_def_diff"] = df_v2["r_td_def"] - df_v2["b_td_def"]

df_v2["sub_avg_diff"] = df_v2["r_sub_avg"] - df_v2["b_sub_avg"]


# In[30]:


diff_features = [
    "wins_diff",
    "losses_diff",
    "height_diff",
    "weight_diff",
    "reach_diff",
    "splm_diff",
    "str_acc_diff",
    "sapm_diff",
    "str_def_diff",
    "td_avg_diff",
    "td_acc_diff",
    "td_def_diff",
    "sub_avg_diff",
    "title_fight"
]

division_columns = [
    col for col in df_v2.columns
    if col.startswith("division_")
]

X_v2 = df_v2[diff_features + division_columns]
y_v2 = df_v2["target"]

print(X_v2.shape)


# In[32]:


X_train_v2, X_test_v2, y_train_v2, y_test_v2 = train_test_split(
    X_v2,
    y_v2,
    test_size=0.2,
    random_state=42,
    stratify=y_v2
)

rf_v2 = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rf_v2.fit(X_train_v2, y_train_v2)

preds_v2 = rf_v2.predict(X_test_v2)

accuracy_v2 = accuracy_score(y_test_v2, preds_v2)

print("Model V1 Accuracy:", accuracy)
print("Model V2 Accuracy:", accuracy_v2)


# In[33]:


from sklearn.metrics import classification_report

print(classification_report(y_test, preds))


# In[34]:


mirror_df = df.copy()

# Swap red and blue fighter stats

swap_pairs = [
    ("r_wins", "b_wins"),
    ("r_losses", "b_losses"),
    ("r_height", "b_height"),
    ("r_weight", "b_weight"),
    ("r_reach", "b_reach"),
    ("r_splm", "b_splm"),
    ("r_str_acc", "b_str_acc"),
    ("r_sapm", "b_sapm"),
    ("r_str_def", "b_str_def"),
    ("r_td_avg", "b_td_avg"),
    ("r_td_avg_acc", "b_td_avg_acc"),
    ("r_td_def", "b_td_def"),
    ("r_sub_avg", "b_sub_avg")
]

for r_col, b_col in swap_pairs:
    mirror_df[r_col] = df[b_col]
    mirror_df[b_col] = df[r_col]

# Reverse target
mirror_df["target"] = 1 - df["target"]


# In[35]:


balanced_df = pd.concat(
    [df, mirror_df],
    ignore_index=True
)

print(balanced_df.shape)

print(
    balanced_df["target"]
    .value_counts(normalize=True)
)


# In[36]:


X_balanced = balanced_df.drop(columns=["target"])
y_balanced = balanced_df["target"]

print(X_balanced.shape)
print(y_balanced.shape)


# In[37]:


from sklearn.model_selection import train_test_split

X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
    X_balanced,
    y_balanced,
    test_size=0.2,
    random_state=42,
    stratify=y_balanced
)

print(X_train_b.shape)
print(X_test_b.shape)


# In[38]:


from sklearn.ensemble import RandomForestClassifier

rf_balanced_data = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rf_balanced_data.fit(X_train_b, y_train_b)

preds_b = rf_balanced_data.predict(X_test_b)


# In[39]:


from sklearn.metrics import accuracy_score, classification_report

print("Balanced Dataset Accuracy:",
      accuracy_score(y_test_b, preds_b))

print(classification_report(y_test_b, preds_b))


# In[40]:


from sklearn.model_selection import train_test_split

# Split original fights first
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["target"]
)

print(train_df.shape)
print(test_df.shape)


# In[41]:


def mirror_fights(source_df):
    mirrored = source_df.copy()

    swap_pairs = [
        ("r_wins", "b_wins"),
        ("r_losses", "b_losses"),
        ("r_height", "b_height"),
        ("r_weight", "b_weight"),
        ("r_reach", "b_reach"),
        ("r_splm", "b_splm"),
        ("r_str_acc", "b_str_acc"),
        ("r_sapm", "b_sapm"),
        ("r_str_def", "b_str_def"),
        ("r_td_avg", "b_td_avg"),
        ("r_td_avg_acc", "b_td_avg_acc"),
        ("r_td_def", "b_td_def"),
        ("r_sub_avg", "b_sub_avg")
    ]

    for r_col, b_col in swap_pairs:
        mirrored[r_col] = source_df[b_col].values
        mirrored[b_col] = source_df[r_col].values

    mirrored["target"] = 1 - source_df["target"].values

    return pd.concat(
        [source_df, mirrored],
        ignore_index=True
    )


# In[42]:


train_balanced = mirror_fights(train_df)
test_balanced = mirror_fights(test_df)

print(train_balanced.shape)
print(test_balanced.shape)

print(train_balanced["target"].value_counts(normalize=True))
print(test_balanced["target"].value_counts(normalize=True))


# In[43]:

from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def add_difference_features(source_df):
    result = source_df.copy()

    feature_pairs = {
        "wins_diff": ("r_wins", "b_wins"),
        "losses_diff": ("r_losses", "b_losses"),
        "height_diff": ("r_height", "b_height"),
        "weight_diff": ("r_weight", "b_weight"),
        "reach_diff": ("r_reach", "b_reach"),
        "splm_diff": ("r_splm", "b_splm"),
        "str_acc_diff": ("r_str_acc", "b_str_acc"),
        "sapm_diff": ("r_sapm", "b_sapm"),
        "str_def_diff": ("r_str_def", "b_str_def"),
        "td_avg_diff": ("r_td_avg", "b_td_avg"),
        "td_acc_diff": ("r_td_avg_acc", "b_td_avg_acc"),
        "td_def_diff": ("r_td_def", "b_td_def"),
        "sub_avg_diff": ("r_sub_avg", "b_sub_avg"),
    }

    for new_column, (red_column, blue_column) in feature_pairs.items():
        result[new_column] = result[red_column] - result[blue_column]

    return result


train_final = add_difference_features(train_balanced)
test_final = add_difference_features(test_balanced)

difference_features = [
    "wins_diff",
    "losses_diff",
    "height_diff",
    "weight_diff",
    "reach_diff",
    "splm_diff",
    "str_acc_diff",
    "sapm_diff",
    "str_def_diff",
    "td_avg_diff",
    "td_acc_diff",
    "td_def_diff",
    "sub_avg_diff",
]

division_features = [
    column
    for column in train_final.columns
    if column.startswith("division_")
]

feature_columns = (
    difference_features
    + ["title_fight"]
    + division_features
)

X_train_final = train_final[feature_columns].copy()
y_train_final = train_final["target"].copy()

X_test_final = test_final[feature_columns].copy()
y_test_final = test_final["target"].copy()

rf_final_v2 = RandomForestClassifier(
    n_estimators=500,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=4,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_final_v2.fit(X_train_final, y_train_final)

preds_final_v2 = rf_final_v2.predict(X_test_final)

print(
    "V2 mirror-safe test accuracy:",
    accuracy_score(y_test_final, preds_final_v2)
)

print(classification_report(y_test_final, preds_final_v2))

feature_importance = (
    pd.DataFrame({
        "feature": feature_columns,
        "importance": rf_final_v2.feature_importances_,
    })
    .sort_values("importance", ascending=False)
    .reset_index(drop=True)
)

print("\nFeature importance:")
print(feature_importance.to_string(index=False))

project_root = Path.cwd()

if project_root.name == "notebooks":
    project_root = project_root.parent

models_dir = project_root / "models"
models_dir.mkdir(parents=True, exist_ok=True)

model_path = models_dir / "kombat_ai_rf_v2.pkl"
features_path = models_dir / "kombat_ai_rf_v2_features.pkl"
importance_path = models_dir / "kombat_ai_rf_v2_feature_importance.csv"

joblib.dump(rf_final_v2, model_path)
joblib.dump(feature_columns, features_path)
feature_importance.to_csv(importance_path, index=False)

print("\nSaved model:", model_path)
print("Saved feature list:", features_path)
print("Saved feature importance:", importance_path)

# In[48]:


import os

os.listdir("../models")


# In[ ]:




