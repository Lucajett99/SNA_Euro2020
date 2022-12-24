import os
from csv import reader
import pandas as pd

def split_name(filename):
    team = filename.split("_")[0]
    opposite_team = filename.split("_")[3].replace(".csv", "")
    match = ""
    if(team == opposite_team):
        opposite_team = filename.split("_")[2]
        match = opposite_team + "_" + team
    else:
        match = team + "_" + opposite_team
    return team, match

def createMetrics(filename, df):
    path = f'./graphsNoSubs/{filename}'
    data = open(path, 'r', encoding='utf-8')
    next(data, None) #skip first line

    centrality_dict = {} #{name: "", cos: 0, cis: 0}
    max_tie = 0 #The highest number of passes between two players
    max_cos = 0
    max_cis = 0
    total_passes = 0

    #Compute Cos & Cis
    with data as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            passer = row[0]
            receiver = row[1]
            n_passes = int(row[2])
            #If the player who made the pass is not in the dictionary, add it
            if(passer not in centrality_dict):
                centrality_dict[passer] = {"cos": n_passes, "cis": 0}
            #else update the cos value
            else:
                centrality_dict[passer]["cos"] = int(centrality_dict[passer]["cos"]) + n_passes
            
            #If the player who receive the pass is not in the dictionary, add it
            if(receiver not in centrality_dict):
                centrality_dict[receiver] = {"cos": 0, "cis": n_passes}
            #else update the cis value
            else:
                centrality_dict[receiver]["cis"] = int(centrality_dict[receiver]["cis"]) + n_passes
            if(max_cos < int(centrality_dict[passer]["cos"])):
                    max_cos = int(centrality_dict[passer]["cos"])
            if(max_cis < int(centrality_dict[receiver]["cis"])):
                    max_cis = int(centrality_dict[receiver]["cis"])
            # row variable is a list that represents a row in csv
            total_passes = total_passes + n_passes
            if(n_passes > max_tie):
                max_tie = n_passes
        
    network_intensity = total_passes #TODO: Normalize network intensity for team possession time or percentage of possession

    data = open(path, 'r', encoding='utf-8')
    next(data, None) #skip first line

    #Compute the weight centralization
    weight_centralization = 0
    number_of_players = len(centrality_dict)
    with data as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            weight_centralization = weight_centralization + max_tie - n_passes
    weight_centralization = weight_centralization / ((number_of_players * (number_of_players - 1) -1) * total_passes)

    #Compute CI & CO
    Ci = 0 # is highest when one player receives all passes and lowest when every member of the team receives an equal number of passes
    Co = 0 # highest when one player makes all the passes and lowest when every member of the team makes the same number of passes.

    for player in centrality_dict:
        Ci = Ci + (max_cis - centrality_dict[player]["cis"])
        Co = Co + (max_cos - centrality_dict[player]["cos"])

    Ci = Ci / ((number_of_players - 1) * total_passes)
    Co = Co / ((number_of_players -1) * total_passes)

    team, match = split_name(filename) #extract team_name and match_name from path

    #create a new row with the metrics of the match
    metrics =  { "team": [team], "match": [match], "Ci": [Ci], "Co": [Co], "weight_centralization": [weight_centralization], "network_intensity": [network_intensity]}
    #convert the dictionary in a dataframe
    df_new_row = pd.DataFrame(metrics, columns = ['team', 'match', 'Ci', 'Co', 'weight_centralization', 'network_intensity'])
    #add the new row to the dataframe
    df = pd.concat([df, df_new_row], axis=0, ignore_index=True)
    return df

#create a dataframe with all metrics
def createStatistics(df):
    metrics = ['Ci', 'Co', 'weight_centralization', 'network_intensity']
    #create an empty dataframe
    df_statistics = pd.DataFrame(columns = ['Mean', 'Std_dev', 'Min', 'Max', 'Obs'])

    for metric in metrics:
        #create a new row with the statistics of the metric
        new_row = {'Mean': [df[metric].mean()], 'Std_dev': [df[metric].std()], 'Min': [df[metric].min()], 'Max': [df[metric].max()], 'Obs': [df[metric].count()]}
        #convert the dictionary in a dataframe
        df_new_row = pd.DataFrame(new_row, columns = ['Mean', 'Std_dev', 'Min', 'Max', 'Obs'])
        #add the new row to the dataframe
        df_statistics = pd.concat([df_statistics, df_new_row], axis=0, ignore_index=True)
    df_statistics.index = metrics
    return df_statistics

def main():
    #create an empty dataframe
    df = pd.DataFrame(columns = ['team', 'match', 'Ci', 'Co', 'weight_centralization', 'network_intensity'])
    #iterate over all the files in the folder for take all matches
    for filename in os.listdir('./graphsNoSubs'):
        #create the metrics for each match and add them to an unique dataframe
        df = createMetrics(filename, df)
    if not os.path.exists('./metrics'):
        os.mkdir('./metrics')
    #save the dataframe in csv and excel format
    df.to_csv(f"./metrics/AllMetrics.csv", index=False)
    df.to_excel(f"./metrics/AllMetrics.xlsx", index=False)
    #create the statistics for each metric and add them to an unique dataframe (statistics)
    df_statistics = createStatistics(df)
    print(df_statistics)
    
#compute mean of the metrics for each team
def computeMean(df):
    #create an empty dataframe
    df_mean = pd.DataFrame(columns = ['team', 'Ci', 'Co', 'weight_centralization', 'network_intensity'])
    #iterate over all the teams
    for team in df['team'].unique():
        #create a new row with the mean of the metrics for each team
        new_row = {'team': [team], 'Ci': [df[df['team'] == team]['Ci'].mean()], 'Co': [df[df['team'] == team]['Co'].mean()], 'weight_centralization': [df[df['team'] == team]['weight_centralization'].mean()], 'network_intensity': [df[df['team'] == team]['network_intensity'].mean()]}
        #convert the dictionary in a dataframe
        df_new_row = pd.DataFrame(new_row, columns = ['team', 'Ci', 'Co', 'weight_centralization', 'network_intensity'])
        #add the new row to the dataframe
        df_mean = pd.concat([df_mean, df_new_row], axis=0, ignore_index=True)
    print(df_mean)
    if not os.path.exists('./metrics'):
        os.mkdir('./metrics')
    #save the dataframe in csv and excel format
    df_mean.to_csv(f"./metrics/MeanMetrics.csv", index=False)
    df_mean.to_excel(f"./metrics/MeanMetrics.xlsx", index=False)
    return df_mean

        


if(__name__ == "__main__"):
    main()


