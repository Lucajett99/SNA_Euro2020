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


match_events = pd.read_excel("./matches/Belgium_Russia_events.xlsx")
side_dict = {"home": match_events.iloc[0]["team"],
             "away": match_events.iloc[1]["team"]}

tactics_home_string = match_events["tactics"].iloc[0].replace("'",'"')
tactics_home = json.loads(tactics_home_string)
lineup_home = tactics_home["lineup"]
print(lineup_home[0])
player_objs_dict = {}
starters = []

for player in lineup_home:
    starters.append(player["player"]["name"]) ##To remove all substitutes from our final grouped_df
    p = Player(player, match_events) ##Calling the Player class
    player_objs_dict.update({player["player"]["name"]: p}) ##For lookup during plotting the grouped_df

total_pass_df = match_events.query("(type == 'Pass') & (pass_type not in ['Free Kick', 'Corner', 'Throw-in', 'Kick Off']) &" f"(team == '{side_dict['home']}') & (pass_outcome not in ['Unknown','Out','Pass Offside','Injury Clearance', 'Incomplete'])")
total_pass_df = total_pass_df.groupby(["player", "pass_recipient"]).size().reset_index(name="count")
total_pass_df = total_pass_df.query(" (player == @starters) & (pass_recipient == @starters) & (count>=@min_pass_count) ")

#print(total_pass_df)
#print(player_objs_dict["Youri Tielemans"])
#print(lineups_away)
arrow_shift = 1 ##Units by which the arrow moves from its original position
shrink_val = 1.5 ##Units by which the arrow is shortened from the end_points

##Visualising the passmap

for row in total_pass_df.itertuples():
    print(row)
    link = row[3] ## for the arrow-width and the alpha
    passer = player_objs_dict[row[1]]
    receiver = player_objs_dict[row[2]]

    alpha = link/15
    if alpha >1:
        alpha=1

    if abs( receiver.x - passer.x) > abs(receiver.y - passer.y):

        if receiver.id > passer.id:
            ax.annotate("", xy=(receiver.x, receiver.y + arrow_shift), xytext=(passer.x, passer.y + arrow_shift),
                            arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw = link*0.12, alpha=alpha))

        elif passer.id > receiver.id:
            ax.annotate("", xy=(receiver.x, receiver.y - arrow_shift), xytext=(passer.x, passer.y - arrow_shift),
                            arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))

    elif abs(receiver.x - passer.x) <= abs(receiver.y - passer.y):

        if receiver.id > passer.id:
            ax.annotate("", xy=(receiver.x + arrow_shift, receiver.y), xytext=(passer.x + arrow_shift, passer.y),
                            arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))

        elif passer.id > receiver.id:
            ax.annotate("", xy=(receiver.x - arrow_shift, receiver.y), xytext=(passer.x - arrow_shift, passer.y),
                            arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))

for name, player in player_objs_dict.items():

    ax.scatter(player.x, player.y, s=player.n_passes_completed*1.3, color=color, zorder = 4)
    ax.text(player.x, player.y+2 if player.y >40 else player.y -2, s=player.name.split(" ")[-1], rotation=270, va="top" if player.y<40 else "bottom", size=6.5, fontweight="book", zorder=7, color=color)

ax.text(124, 80, f"{side_dict['home']}", size=12, fontweight="demibold", rotation=270, color=color, va="top")
ax.text(122, 80, f"{side_dict['home']} vs {side_dict['away']}", size=8, fontweight="demibold", rotation = 270, va="top")

fig.tight_layout()
plt.show()