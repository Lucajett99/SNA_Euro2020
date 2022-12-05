from statsbombpy import sb
import pandas as pd
import os

# Get competitions
comp = sb.competitions()
# Get Matches from Euro2020
df = sb.matches(competition_id=55, season_id=43)

# For all matches 
for index, row in df.iterrows():
<<<<<<< HEAD:NoSubs/ExtractMatches.py
    home_team = row["home_team"]  
    away_team = row["away_team"]
=======
>>>>>>> c5f4f1e60217b8b5836e9c3d6cbe312588d20b2f:Subs/ExtractMatches.py
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

<<<<<<< HEAD:NoSubs/ExtractMatches.py
    subs = []
    for index, row in match_events.iterrows():
        player = row['substitution_replacement']
        if(not pd.isna(player)):
            subs.append(player)
    
    match_events = match_events[(match_events["type"] == "Starting XI") | (match_events["type"]=="Pass")]

    for player in subs:
        match_events = match_events[~match_events['player'].str.contains(player, na=False)]
        match_events = match_events[~match_events['pass_recipient'].str.contains(player, na=False)]

=======
>>>>>>> c5f4f1e60217b8b5836e9c3d6cbe312588d20b2f:Subs/ExtractMatches.py

    # split locations into x and y components
    match_events[['location_x', 'location_y']] = match_events['location'].apply(pd.Series)
    match_events[['pass_end_location_x', 'pass_end_location_y']] = match_events['pass_end_location'].apply(pd.Series)
    match_events.drop(["location", "pass_end_location"], axis=1)
   
    #Get only pass events
    match_events = match_events[(match_events["type"] == "Starting XI") | (match_events["type"]=="Pass")]
<<<<<<< HEAD:NoSubs/ExtractMatches.py
=======
    if not os.path.exists('./matches'):
        os.mkdir('./matches')

    home_team = row["home_team"]  
    away_team = row["away_team"]
>>>>>>> c5f4f1e60217b8b5836e9c3d6cbe312588d20b2f:Subs/ExtractMatches.py
    match_events.to_excel(f'./matches/{home_team}_{away_team}_events.xlsx', index=False)