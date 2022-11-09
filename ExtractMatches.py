from statsbombpy import sb
import pandas as pd
from pandas import json_normalize
import numpy as np

# Get competitions
comp = sb.competitions()
# Get Matches from Euro2020
df = sb.matches(competition_id=55, season_id=43)

# For all matches 
for index, row in df.iterrows():
    #Get the match_id
    match_events = sb.events(match_id=row['match_id'])
    #Create a dummy column pass_goal_assist if not exist to avoid problems
    if not "pass_goal_assist" in match_events:
        match_events['pass_goal_assist'] = ""
    #Get only interesting column
    match_events = match_events[[
        'index', 'match_id', 'minute', 'pass_angle', 'pass_height', 'pass_length', 'pass_outcome',
        'pass_recipient', 'pass_shot_assist', 'period', 'play_pattern', 'player', 'player_id', 'position', 'possession_team_id', 'team', 'timestamp', 'type','location', 'pass_aerial_won',
        'pass_cross', 'pass_end_location', 'pass_goal_assist', 'pass_type', 'play_pattern', 
    'substitution_outcome' ,'substitution_replacement', 'tactics'
    ]]


    # split locations into x and y components
    match_events[['location_x', 'location_y']] = match_events['location'].apply(pd.Series)
    match_events[['pass_end_location_x', 'pass_end_location_y']] = match_events['pass_end_location'].apply(pd.Series)
    match_events.drop(["location", "pass_end_location"], axis=1)
   
    #Get only pass events
    match_events = match_events[match_events[ "type"] == 'Pass']
    home_team = row["home_team"]  
    away_team = row["away_team"]
    match_events.to_excel(f'./matches/{home_team}_{away_team}_events.xlsx', index=False)