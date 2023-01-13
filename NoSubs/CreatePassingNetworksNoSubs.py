import pandas as pd
import json 
import matplotlib.pyplot as plt
import os
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch


def get_teams_name(df):
    # get match teams name
    team1, team2 = df.team.unique()
    return team1, team2

def loadDataset(fileName):
    match_events = pd.read_excel(fileName)
    return match_events

def getLineups(df, side):
    if(side == "home"):
        tactics_string = df["tactics"].iloc[0].replace("'",'"')
    else:
        tactics_string = df["tactics"].iloc[1].replace("'",'"')
    tactics = json.loads(tactics_string)
    lineup = tactics["lineup"]
    lineup = json.dumps(lineup).replace("[", "")
    lineup = lineup.replace("]", "")
    return lineup

def get_pass_df(df, team):
    # boolean mask if the event is pass and team is our team
    team_pass_mask = (df.type == 'Pass') & (df.team == team)
    # create a dataframe of the passes only
    pass_df = df[team_pass_mask]
    return pass_df

def searchID(players_df, index):
    players_df = players_df[players_df.apply(lambda row: row.astype(str).str.contains(index, case=False).any(), axis=1)]
    return players_df.jersey_number.values

def createDicts(df, team, players_df):
    pass_df = get_pass_df(df, team)
    # boolean mask if the pass is completed
    complete_pass_mask = pass_df.pass_outcome.isnull()
    completed_pass = pass_df[complete_pass_mask]
    # players average passes location['location_x'],['location_y'] , player_id => index
    avg_loc = completed_pass.groupby(['player', 'player_id'], as_index=False).agg({'location_x': ['mean'], 'location_y': ['mean']})
    avg_loc.columns = ['player', 'id', 'x', 'y']
    avg_loc = avg_loc.set_index("player")
    # pass between player_id and pass_recipient_id
    pass_between = completed_pass.groupby(['player', 'pass_recipient'], as_index=False).index.count()
    pass_between.columns = ['passer', 'recipient', 'n_passes_completed']
    #merge avg_loc table with pass_between table throw passer column to get start['location_x'],['location_y']
    #pass_between = pass_between.merge(avg_loc, left_on='passer', right_index=True)
    # merge avg_loc table with pass_between table throw recipient column to get end['location_x'],['location_y']
    #pass_between = pass_between.merge(avg_loc, left_on='recipient', right_index=True, suffixes=['', '_end'])
    pass_completed = completed_pass.groupby('player', as_index=False).index.count()
    pass_completed.columns = ['player', 'n_passes_completed']
    pass_completed = pass_completed.set_index('player')
    avg_loc = avg_loc.join(pass_completed, on='player')
    df_avg_loc = avg_loc
    avg_loc = avg_loc.to_dict('index')
    return pass_between, avg_loc, df_avg_loc

def plotPassingNetwork(pass_between, avg_loc,  home_team, away_team, side):
    #if not os.path.exists(f"./imgWithoutSubs/{away_team}_Network_{home_team}_{away_team}.png"):
    color = "blue"
    min_pass_count = 2 ##minimum number of passes for a link to be plotted
    pitch = Pitch()
    # specifying figure size (width, height)
    fig, ax = pitch.draw(figsize=(8, 4))
    arrow_shift = 1 ##Units by which the arrow moves from its original position
    shrink_val = 1.5 ##Units by which the arrow is shortened from the end_points 
    for row in pass_between.itertuples():
        if( row[2] in avg_loc.keys()):
            n_passBetween = row[3] ## for the arrow-width and the alpha
            passer = avg_loc[row[1]]
            receiver = avg_loc[row[2]]

            alpha = n_passBetween/15
            if alpha >1:
                alpha=1

            if abs( receiver['x'] - passer['x']) > abs(receiver['y'] - passer['y']):

                if receiver['id'] > passer['id']:
                    ax.annotate("", xy=(receiver['x'], receiver['y'] + arrow_shift), xytext=(passer['x'], passer['y'] + arrow_shift),
                                    arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw = n_passBetween*0.12, alpha=alpha))

                elif passer['id'] > receiver['id']:
                    ax.annotate("", xy=(receiver['x'], receiver['y'] - arrow_shift), xytext=(passer['x'], passer['y'] - arrow_shift),
                                    arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=n_passBetween*0.12, alpha=alpha))

            elif abs(receiver['x'] - passer['x']) <= abs(receiver['y'] - passer['y']):

                if receiver['id'] > passer['id']:
                    ax.annotate("", xy=(receiver['x'] + arrow_shift, receiver['y']), xytext=(passer['x'] + arrow_shift, passer['y']),
                                    arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=n_passBetween*0.12, alpha=alpha))

                elif passer['id'] > receiver['id']:
                    ax.annotate("", xy=(receiver['x'] - arrow_shift, receiver['y']), xytext=(passer['x'] - arrow_shift, passer['y']),
                                    arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=n_passBetween*0.12, alpha=alpha))

        for name, player in avg_loc.items():
            ax.scatter(player['x'], player['y'], s=player['n_passes_completed']*1.7, color="red", zorder = 4)
            ax.text(player['x'], player['y']+11 if player['y'] > 40 else player['y'] -11, s=name.split(" ")[-1], rotation=270, va="top" if player['y']<40 else "bottom", size=6.5, fontweight="book", zorder=7, color="black")
        fig.tight_layout()
    
    if (side == "home"):
        plt.savefig(f"./ImagesToRedo/{home_team}_Network_{home_team}_{away_team}.png")
    else:
        plt.savefig(f"./ImagesToRedo/{away_team}_Network_{home_team}_{away_team}.png")

def main():
    # Get Matches from Euro2020
    if not os.path.exists('./imgWithoutSubs'):
            os.mkdir('./imgWithoutSubs')
    #df = sb.matches(competition_id=55, season_id=43)
    #for  index, row in df.iterrows():
    home_team ="Italy" #row["home_team"]  
    away_team = "Switzerland" #row["away_team"]
    match_events = loadDataset(f"./matchesNoSubs/{home_team}_{away_team}_events.xlsx")
    homeTeamName, awayTeamName = get_teams_name(match_events)
    print(home_team + "\t" + away_team)
    homeLineup = getLineups(match_events, "home")    
    homeLineupDF = pd.read_json(homeLineup, lines=True)
    pass_betweenHome, avg_locHome, df_avg_locHome = createDicts(match_events, homeTeamName, homeLineupDF)
    plotPassingNetwork(pass_betweenHome, avg_locHome, home_team, away_team, "home")
    print("in")
    awayLineup = getLineups(match_events, "away")
    awayLineupDF = pd.read_json(awayLineup, lines=True)
    pass_betweenAway, avg_locAway, df_avg_locAway = createDicts(match_events, awayTeamName, awayLineupDF)
    #plotPassingNetwork(pass_betweenAway, avg_locAway,  home_team, away_team, "away")
    #print(pass_betweenHome, pass_betweenAway)
    if not os.path.exists('./graphsNoSubs'):
        os.mkdir('./graphsNoSubs')
    
    #csv = df = pd.read_json(avg_locHome)
    #pass_betweenHome.to_csv(f"./graphsNoSubs/{home_team}_Passes_{home_team}_{away_team}.csv", index=False)
    #pass_betweenAway.to_csv(f"./graphsNoSubs/{away_team}_Passes_{home_team}_{away_team}.csv", index=False)
        

        
if(__name__ == "__main__"):
    main()