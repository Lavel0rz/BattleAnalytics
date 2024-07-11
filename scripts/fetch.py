
import os
import requests
import pandas as pd

# Function to fetch and process data for a specific round
def fetch_and_process_data(round_index, is_losers):
    url = "https://gotchi-battler-backend-blmom6tkla-ew.a.run.app/api/v1/tournaments/14/brackets"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if is_losers:
            rounds = data[1]['rounds'][round_index]
            round_prefix = "losers_brackets_"
            csv_name = rounds['name'].replace(' ', '').lower()
        else:
            rounds = data[0]['rounds'][round_index]
            round_prefix = "brackets_"

        csv_name = rounds['name'].replace(' ', '').lower()
        battles = rounds['battles']

        battle_data = []
        for battle in battles:
            battle_id = battle['id']
            team1_id = battle['team1Id']
            team2_id = battle['team2Id']
            round_name = rounds['name']
            battle_data.append([round_name, battle_id, team1_id, team2_id])

        df = pd.DataFrame(battle_data, columns=['Round Name', 'Battle ID', 'Team 1 ID', 'Team 2 ID'])

        # Check if the CSV already exists to prevent overwriting
        csv_filename = f'{round_prefix}{csv_name}.csv'
        if not os.path.exists(csv_filename):
            df.to_csv(csv_filename, index=False)

        result_df = pd.DataFrame(columns=['Team ID', 'Team Name'] + [f'{pos} Gotchi Special ID' for pos in gotchi_positions])

        for battle_id in df['Battle ID']:
            battle_url = f"https://gotchi-battler-backend-blmom6tkla-ew.a.run.app/api/v1/battles/{battle_id}"
            response = requests.get(battle_url)

            if response.status_code == 200:
                battle_data = response.json()
                for team_key in ['team1', 'team2']:
                    team = battle_data.get(team_key)
                    if team is None:
                        team_data = {'Team ID': 'BYE', 'Team Name': 'BYE'}
                        for pos in gotchi_positions:
                            team_data[f'{pos} Gotchi Special ID'] = None
                    else:
                        team_data = {'Team ID': team['id'], 'Team Name': team['name']}
                        for pos in gotchi_positions:
                            gotchi = team.get(f'{pos}Gotchi')
                            team_data[f'{pos} Gotchi Special ID'] = extract_gotchi_special_id(gotchi)

                    team_df = pd.DataFrame([team_data])
                    result_df = pd.concat([result_df, team_df], ignore_index=True)

        merged_df = df.copy()
        result_df_team1 = result_df.add_prefix('Team 1 ').rename(columns={'Team 1 Team ID': 'Team 1 ID'})
        result_df_team2 = result_df.add_prefix('Team 2 ').rename(columns={'Team 2 Team ID': 'Team 2 ID'})

        merged_df = merged_df.merge(result_df_team1, on='Team 1 ID', how='left')
        merged_df = merged_df.merge(result_df_team2, on='Team 2 ID', how='left')

        # Check if the result CSV already exists to prevent overwriting
        result_csv_filename = f'{round_prefix}{csv_name}_result.csv'
        if not os.path.exists(result_csv_filename):
            merged_df.to_csv(result_csv_filename)

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def extract_gotchi_special_id(gotchi):
    return gotchi['specialId'] if gotchi else None

# List of gotchi positions to check
gotchi_positions = ['front1', 'front2', 'front3', 'front4', 'front5',
                    'back1', 'back2', 'back3', 'back4', 'back5',
                    'leader', 'sub1', 'sub2']

# Fetch and process data for the next rounds
fetch_and_process_data(5, False) # For the next winners bracket round
fetch_and_process_data(4, True)  # For the next losers bracket round

