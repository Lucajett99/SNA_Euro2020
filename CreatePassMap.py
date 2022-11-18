import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from pandas import json_normalize
from pandas.core.common import SettingWithCopyWarning
from mplsoccer import Pitch, VerticalPitch


color = "blue"
min_pass_count = 2 ##minimum number of passes for a link to be plotted

pitch = Pitch()
# specifying figure size (width, height)
fig, ax = pitch.draw(figsize=(8, 4))


class Player:
    def __init__(self,player, df):
        self.id = player["player"]["id"]
        self.name = player["player"]["name"]
        self.average_position(df)

    def average_position(self, df):

        player_pass_df = df.query("(pass_type not in ['Free Kick', 'Corner', 'Throw-in', 'Kick Off']) & (player_id == @self.id) & (pass_outcome not in ['Unknown','Out','Pass Offside','Injury Clearance', 'Incomplete'])")
        self.x  = np.mean(player_pass_df['location_x'], axis=0)
        self.y  = np.mean(player_pass_df['location_y'], axis=0)

        self.n_passes_completed = len(player_pass_df)


match_events = pd.read_excel("./matches/Italy_Spain_events.xlsx")
side_dict = {"home": match_events.iloc[0]["team"],
             "away": match_events.iloc[1]["team"]}

tactics_home_string = match_events["tactics"].iloc[0].replace("'",'"')
tactics_home = json.loads(tactics_home_string)
lineup_home = tactics_home["lineup"]
print(lineup_home)
player_objs_dict = {}
starters = []

for player in lineup_home:
    starters.append(player["player"]["name"]) ##To remove all substitutes from our final grouped_df
    p = Player(player, match_events) ##Calling the Player class
    player_objs_dict.update({player["player"]["name"]: p}) ##For lookup during plotting the grouped_df

total_pass_df = match_events.query("(type == 'Pass') & (pass_type not in ['Free Kick', 'Corner', 'Throw-in', 'Kick Off']) &" f"(team == '{side_dict['home']}') & (pass_outcome not in ['Unknown','Out','Pass Offside','Injury Clearance', 'Incomplete'])")
total_pass_df = total_pass_df.groupby(["player", "pass_recipient"]).size().reset_index(name="count")
total_pass_df = total_pass_df.query(" (player == @starters) & (pass_recipient == @starters) & (count>=@min_pass_count) ")

print(total_pass_df)
#print(lineups_away)