from statsbombpy import sb
import pandas as pd
import os
import numpy as np

# Get competitions
comp = sb.competitions()
# Get Matches from Euro2020
df = sb.matches(competition_id=55, season_id=43)

df_possession = pd.DataFrame(columns=['team', 'match', 'possession_minutes', 'possession_percentage'])

# For all matches 
for index, row in df.iterrows():
    home_team = row["home_team"]  
    away_team = row["away_team"]
    home_score = row["home_score"]
    away_score = row["away_score"]
    match = home_team + "_" + away_team
    #Get the match_id
    match_events = sb.events(match_id=row['match_id'])

    #calculate the possession time (in minutes) of each team
    duration = match_events.groupby(['team']).sum()['duration'].to_dict()
    duration[home_team] = duration[home_team] / 60
    duration[away_team] = duration[away_team] / 60

    #calculate the possession percentage of each team
    total_minutes = duration[home_team] + duration[away_team]
    home_percentage = (duration[home_team] / total_minutes)*100
    away_percentage = (duration[away_team] / total_minutes)*100

    #create two dictionaries, one for each team
    home_row = {'team': home_team, 'match': [match], 'possession_minutes': [duration[home_team]], 'possession_percentage': [home_percentage], 'goal_scored': [home_score]}
    away_row = {'team': away_team, 'match': [match], 'possession_minutes': [duration[away_team]], 'possession_percentage': [away_percentage], 'goal_scored': [away_score]}
    #convert the dictionaries to dataframes
    df_home_row = pd.DataFrame(home_row, columns = ['team', 'match', 'possession_minutes', 'possession_percentage', 'goal_scored'])
    df_away_row = pd.DataFrame(away_row, columns = ['team', 'match', 'possession_minutes', 'possession_percentage', 'goal_scored'])
    #concatenate the two dataframes to the main dataframe
    df_possession = pd.concat([df_possession, df_home_row], axis=0, ignore_index=True)
    df_possession = pd.concat([df_possession, df_away_row], axis=0, ignore_index=True)

#read the metrics file and add the possession with a merge
allMetrics = pd.read_excel('./metrics/AllMetrics.xlsx')
allMetrics = allMetrics.merge(df_possession, on=['team', 'match'], how='left')

#add two new columns for the normalized values, one with minutes and one with percentage
allMetrics['I_normalized_minutes'] = np.nan
allMetrics['I_normalized_percentage'] = np.nan

#normalize the intensity values with the possession time and percentage
for index, row in allMetrics.iterrows():
    intensity = row['network_intensity']
    possession_minutes = row['possession_minutes']
    possession_percentage = row['possession_percentage']
    allMetrics.at[index,'I_normalized_minutes'] = intensity / possession_minutes
    allMetrics.at[index,'I_normalized_percentage'] = intensity / possession_percentage

#save the new metrics file
allMetrics.to_excel('./metrics/AllMetricsPossession.xlsx', index=False)
allMetrics.to_csv('./metrics/AllMetricsPossession.csv', index=False)



