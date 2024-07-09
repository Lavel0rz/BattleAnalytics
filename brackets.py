import streamlit as st
import pandas as pd

st.title('Battler Analyzer')


battle_id = st.text_input('Analize Battle!' , placeholder= 'Input BattleID')
df = pd.read_csv("brackets.csv")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Define the type mapping
type_mapping = {
    '1': 'Ninja',
    '2': 'Enlightened',
    '3': 'Cleaver',
    '4': 'Tank',
    '5': 'Cursed',
    '6': 'Healer',
    '7': 'Mage',
    '8': 'Troll'
}

color_map = {
    '1': 'cyan',
    '2': 'pink',
    '3': 'red',
    '4': 'orange',
    '5': 'grey',
    '6': 'yellow',
    '7': 'purple',
    '8': 'green'
}

def create_custom_colormap(color_map):
    # Make sure all classes are present in color_map
    classes = list(color_map.keys())
    colors = [color_map[cls] for cls in classes]
    
    # Create a custom color map
    return LinearSegmentedColormap.from_list('custom_colormap', colors, N=len(colors))

custom_cmap = create_custom_colormap(color_map)

# Define the leader marker
leader_marker = ''

# Read the CSV files
df1 = pd.read_csv('brackets.csv')
df2 = pd.read_csv('brackets2.csv')

# Define the round ID to focus on
round_id = battle_id

# Filter the dataframes for the given round ID
df1_filtered = df1[df1['Battle ID'] == round_id]
df2_filtered = df2[df2['Battle ID'] == round_id]

# Ensure the columns are in the same order and filter rows by Round ID
df2_filtered = df2_filtered[df1_filtered.columns]

# Compare the two filtered dataframes and find the differences
diff = df1_filtered.compare(df2_filtered, keep_equal=True)

# Prepare matrices for front and back Gotchi positions
front_positions = ['front1', 'front2', 'front3', 'front4', 'front5']
back_positions = ['back1', 'back2', 'back3', 'back4', 'back5']

# Initialize matrices for Team 1
matrix_self_team1 = np.full((2, 5), np.nan)
matrix_other_team1 = np.full((2, 5), np.nan)
matrix_diff_team1 = np.full((2, 5), np.nan)

# Initialize matrices for Team 2
matrix_self_team2 = np.full((2, 5), np.nan)
matrix_other_team2 = np.full((2, 5), np.nan)
matrix_diff_team2 = np.full((2, 5), np.nan)

# Initialize leader detection arrays
leader_team1 = np.full((2, 5), False)
leader_team2 = np.full((2, 5), False)

def handle_nan(value):
    if pd.isna(value):
        return ''
    elif isinstance(value, float):
        return str(int(value))
    else:
        return str(value)

# Fill matrices for Team 1 and detect leaders
for pos in front_positions:
    col_name = f'Team 1 {pos} Gotchi Special ID'
    idx = front_positions.index(pos)
    if col_name in df1_filtered.columns:
        self_value = df1_filtered[col_name].values[0]
        other_value = df2_filtered[col_name].values[0]
        matrix_self_team1[0, idx] = self_value
        matrix_other_team1[0, idx] = other_value
        if col_name in diff.columns.levels[0]:
            matrix_diff_team1[0, idx] = diff[col_name]['self'].values[0] if not np.isnan(diff[col_name]['self'].values[0]) else np.nan
        
        # Check if this Gotchi is a Leader
        if not pd.isna(self_value) and df1_filtered.filter(like='leader').iloc[0].astype(str).astype(float).astype(int).isin([self_value]).any():
            leader_team1[0, idx] = True

for pos in back_positions:
    col_name = f'Team 1 {pos} Gotchi Special ID'
    idx = back_positions.index(pos)
    if col_name in df1_filtered.columns:
        self_value = df1_filtered[col_name].values[0]
        other_value = df2_filtered[col_name].values[0]
        matrix_self_team1[1, idx] = self_value
        matrix_other_team1[1, idx] = other_value
        if col_name in diff.columns.levels[0]:
            matrix_diff_team1[1, idx] = diff[col_name]['self'].values[0] if not np.isnan(diff[col_name]['self'].values[0]) else np.nan
        
        # Check if this Gotchi is a Leader
        if not pd.isna(self_value) and df1_filtered.filter(like='leader').iloc[0].astype(str).astype(float).astype(int).isin([self_value]).any():
            leader_team1[1, idx] = True

# Fill matrices for Team 2 and detect leaders
for pos in front_positions:
    col_name = f'Team 2 {pos} Gotchi Special ID'
    idx = front_positions.index(pos)
    if col_name in df1_filtered.columns:
        self_value = df1_filtered[col_name].values[0]
        other_value = df2_filtered[col_name].values[0]
        matrix_self_team2[0, idx] = self_value
        matrix_other_team2[0, idx] = other_value
        if col_name in diff.columns.levels[0]:
            matrix_diff_team2[0, idx] = diff[col_name]['self'].values[0] if not np.isnan(diff[col_name]['self'].values[0]) else np.nan
        
        # Check if this Gotchi is a Leader
        if not pd.isna(self_value) and df1_filtered.filter(like='leader').iloc[0].astype(str).astype(float).astype(int).isin([self_value]).any():
            leader_team2[0, idx] = True

for pos in back_positions:
    col_name = f'Team 2 {pos} Gotchi Special ID'
    idx = back_positions.index(pos)
    if col_name in df1_filtered.columns:
        self_value = df1_filtered[col_name].values[0]
        other_value = df2_filtered[col_name].values[0]
        matrix_self_team2[1, idx] = self_value
        matrix_other_team2[1, idx] = other_value
        if col_name in diff.columns.levels[0]:
            matrix_diff_team2[1, idx] = diff[col_name]['self'].values[0] if not np.isnan(diff[col_name]['self'].values[0]) else np.nan
        
        # Check if this Gotchi is a Leader
        if not pd.isna(self_value) and df1_filtered.filter(like='leader').iloc[0].astype(str).astype(float).astype(int).isin([self_value]).any():
            leader_team2[1, idx] = True


def get_leader_class(df, team):
    leader_col = f'{team} leader Gotchi Special ID'
    if leader_col in df.columns:
        leader_id = df[leader_col].values[0]
        return type_mapping.get(handle_nan(leader_id), 'Unknown')
    return 'None'

# Extract leader classes for each team
leader_team1_pre = get_leader_class(df1_filtered, 'Team 1')
leader_team1_battle = get_leader_class(df2_filtered, 'Team 1')
leader_team2_pre = get_leader_class(df1_filtered, 'Team 2')
leader_team2_battle = get_leader_class(df2_filtered, 'Team 2')

# Define the range of your data
vmin = 1
vmax = 8

# Create a normalizer with the defined range
norm = Normalize(vmin=vmin, vmax=vmax)

# Plot the matrices as heatmaps
fig, axes = plt.subplots(4, 1, figsize=(12, 16), sharex=True)

# Plot for Team 1
sns.heatmap(matrix_self_team1, annot=False, cmap=custom_cmap, ax=axes[0], cbar=False, norm=norm)
axes[0].set_title(f'Team 1 Pre-Round Gotchi Positions (Leader: {leader_team1_pre})')
axes[0].set_ylabel('Row')
axes[0].set_yticklabels(['Front', 'Back'])
axes[0].set_xticklabels(['1', '2', '3', '4', '5'])

sns.heatmap(matrix_other_team1, annot=False, cmap=custom_cmap, ax=axes[1], cbar=False, norm=norm)
axes[1].set_title(f'Team 1 Battle Gotchi Positions (with Changes) (Leader: {leader_team1_battle})')
axes[1].set_xlabel('Position')
axes[1].set_ylabel('Row')
axes[1].set_xticklabels(['1', '2', '3', '4', '5'])
axes[1].set_yticklabels(['Front', 'Back'])

# Plot for Team 2
sns.heatmap(matrix_self_team2, annot=False, cmap=custom_cmap, ax=axes[2], cbar=False, norm=norm)
axes[2].set_title(f'Team 2 Pre-Round Gotchi Positions (Leader: {leader_team2_pre})')
axes[2].set_ylabel('Row')
axes[2].set_yticklabels(['Front', 'Back'])
axes[2].set_xticklabels(['1', '2', '3', '4', '5'])

sns.heatmap(matrix_other_team2, annot=False, cmap=custom_cmap, ax=axes[3], cbar=False, norm=norm)
axes[3].set_title(f'Team 2 Battle Gotchi Positions (with Changes) (Leader : {leader_team2_battle})')
axes[3].set_xlabel('Position')
axes[3].set_ylabel('Row')
axes[3].set_xticklabels(['1', '2', '3', '4', '5'])
axes[3].set_yticklabels(['Front', 'Back'])

# Annotate the heatmaps with the class names and Leader markers
for i in range(2):
    for j in range(5):
        # Annotate Team 1 heatmaps
        class_self_team1 = type_mapping.get(handle_nan(matrix_self_team1[i, j]), '') if not pd.isna(matrix_self_team1[i, j]) else ''
        class_other_team1 = type_mapping.get(handle_nan(matrix_other_team1[i, j]), '') if not pd.isna(matrix_other_team1[i, j]) else ''
        axes[0].text(j + 0.5, i + 0.5, f'{class_self_team1}{" " + leader_marker if leader_team1[i, j] else ""}', ha='center', va='center', color='white')
        axes[1].text(j + 0.5, i + 0.5, f'{class_other_team1}{" " + leader_marker if leader_team1[i, j] else ""}', ha='center', va='center', color='white')
        
        # Annotate Team 2 heatmaps
        class_self_team2 = type_mapping.get(handle_nan(matrix_self_team2[i, j]), '') if not pd.isna(matrix_self_team2[i, j]) else ''
        class_other_team2 = type_mapping.get(handle_nan(matrix_other_team2[i, j]), '') if not pd.isna(matrix_other_team2[i, j]) else ''
        axes[2].text(j + 0.5, i + 0.5, f'{class_self_team2}{" " + leader_marker if leader_team2[i, j] else ""}', ha='center', va='center', color='white')
        axes[3].text(j + 0.5, i + 0.5, f'{class_other_team2}{" " + leader_marker if leader_team2[i, j] else ""}', ha='center', va='center', color='white')

plt.tight_layout()
plt.show()

# Print summary of changes
if not any(matrix_diff_team1[~np.isnan(matrix_diff_team1)]):
    print("No changes detected in Team 1 for the given round.")
elif not any(matrix_diff_team2[~np.isnan(matrix_diff_team2)]):
    print("No changes detected in Team 2 for the given round.")
elif not any(matrix_diff_team1[~np.isnan(matrix_diff_team1)]) and not any(matrix_diff_team2[~np.isnan(matrix_diff_team2)]):
    print("No changes detected in Team 1 or Team 2 for the given round.")
else:
    if any(matrix_diff_team1[~np.isnan(matrix_diff_team1)]):
        print("Changes detected in Team 1.")
    if any(matrix_diff_team2[~np.isnan(matrix_diff_team2)]):
        print("Changes detected in Team 2.")


st.pyplot(fig)