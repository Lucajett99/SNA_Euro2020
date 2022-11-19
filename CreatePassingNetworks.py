import pandas as pd
import json 
import matplotlib.pyplot as plt
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

def pass_network(df, team, players_df):
    pass_df = get_pass_df(df, team)
    # boolean mask if the pass is completed
    complete_pass_mask = pass_df.pass_outcome.isnull()
    completed_pass = pass_df[complete_pass_mask]
    # players average passes location['location_x'],['location_y'] , player_id => index
    avg_loc = completed_pass.groupby('player' ).agg({'location_x': ['mean'], 'location_y': ['mean']})
    avg_loc.columns = ['location_x', 'location_y']
    # pass between player_id and pass_recipient_id
    pass_between = completed_pass.groupby(['player', 'pass_recipient'], as_index=False).index.count()
    pass_between.columns = ['passer', 'recipient', 'passes_between']
    # merge avg_loc table with pass_between table throw passer column to get start['location_x'],['location_y']
    pass_between = pass_between.merge(avg_loc, left_on='passer', right_index=True)
    # merge avg_loc table with pass_between table throw recipient column to get end['location_x'],['location_y']
    pass_between = pass_between.merge(avg_loc, left_on='recipient', right_index=True, suffixes=['', '_end'])
    avg_loc = avg_loc.to_dict('index')
    '''
    # setup the pitch
    pitch = Pitch(pitch_color='grass', line_color='white')
    fig, ax = pitch.draw()
    # plot passes network
    pitch.arrows(
        xstart=pass_between['location_x'], ystart=pass_between['location_y'], xend=pass_between.location_x_end,
        yend=pass_between.'location_y'_end, width=1, headwidth=10, headlength=30, color='#990000', ax=ax)
    # plot players
    pitch.scatter(
    ['location_x']=pass_between['location_x'],['location_y']=pass_between['location_y'], s=250, color='red', edgecolor='black', linewidth=1, alpha=1, ax=ax)
    # plot players jersey number
    
    for index, row in avg_loc.iterrows():
        # index in avg_loc table is the player_id
        #player_jersey_number = players_df[players_df.player_id == index].player_jersey_number.values[0]
        player_jersey_number = searchID(players_df, index)
        print(pass_between.head())
        ax.text(row['location_x'], row['location_y']-2 if row['location_y'] > 40 else row['location_y']+2, s=row.name.split(" ")[-1], rotation=270, va="top" if row['location_y']<40 else "bottom", size=8, fontweight="bold", zorder=7, color="white")
        pitch.annotate(player_jersey_number, xy=(row['location_x'], row['location_y']), c='white', va='center', ha='center',
                       size=8, weight='bold', ax=ax)
    ax.set_title(f'{team} Pass Network')
    plt.show()
    '''
    
    pitch = Pitch()
    # specifying figure size (width, height)
    fig, ax = pitch.draw(figsize=(8, 4))
    arrow_shift = 1 ##Units by which the arrow moves from its original position
    shrink_val = 1.5 ##Units by which the arrow is shortened from the end_points

    ##Visualising the passmap
    for row in pass_between.itertuples():
        link = row[3] ## for the arrow-width and the alpha
        passer = avg_loc[row[1]]
        receiver = avg_loc[row[2]]
        alpha = link/15
        '''
        if alpha >1:
            alpha=1
        if abs( receiver['location_x'] - passer['location_x']) > abs(receiver['location_y'] - passer['location_y']):

            if receiver['id'] > passer['id']:
                ax.annotate("", xy=(receiver['location_x'], receiver['location_y'] + arrow_shift), xytext=(passer['location_x'], passer['location_y'] + arrow_shift),
                                arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw = link*0.12, alpha=alpha))

            elif passer['id'] > receiver['id']:
                ax.annotate("", xy=(receiver['location_x'], receiver['location_y'] - arrow_shift), xytext=(passer['location_x'], passer['location_y'] - arrow_shift),
                                arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))

        elif abs(receiver['location_x'] - passer['location_x']) <= abs(receiver['location_y'] - passer['location_y']):

            if receiver['id'] > passer['id']:
                ax.annotate("", xy=(receiver['location_x'] + arrow_shift, receiver['location_y']), xytext=(passer['location_x'] + arrow_shift, passer['location_y']),
                                arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))

            elif passer['id'] > receiver['id']:
                ax.annotate("", xy=(receiver['location_x'] - arrow_shift, receiver['location_y']), xytext=(passer['location_x'] - arrow_shift, passer['location_y']),
                                arrowprops=dict(arrowstyle="-|>", color="0.25", shrinkA=shrink_val, shrinkB=shrink_val, lw=link*0.12, alpha=alpha))
        '''
        
        for row, player in pass_between.iterrows():

            ax.scatter(player['location_x'], player['location_y'], s=player.passes_between*1.3, color="blue", zorder = 4)
            ax.text(player['location_x'], player['location_y']+2 if player['location_y'] >40 else player['location_y'] -2, s=player.passer.split(" ")[-1], rotation=270, va="top" if player['location_y']<40 else "bottom", size=6.5, fontweight="book", zorder=7, color="blue")

        fig.tight_layout()
        plt.show()
        
def main():
    match_events = loadDataset("./matches/Belgium_Russia_events.xlsx")
    homeTeamName, awayTeamName = get_teams_name(match_events)
    homeLineup = getLineups(match_events, "home")
    #awayLineup = getLineups(match_events, "away")
    homeLineupDF = pd.read_json(homeLineup, lines=True)
    #awayLineupDF = pd.read_json(awayLineup, orient='index')
    pass_network(match_events, homeTeamName, homeLineupDF)
    
    #pass_network(match_events, awayTeamName, awayLineupDF)

if(__name__ == "__main__"):
    main()