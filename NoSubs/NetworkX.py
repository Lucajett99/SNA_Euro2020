import networkx as nx
import matplotlib.pyplot as plt
from csv import reader
      

G = nx.DiGraph()
data = open('./graphsNoSubs/Italy_Passes_Italy_Spain.csv', 'r')
next(data, None) #skip first line
total_passes = 0

centrality_dict = {} #{name: "", cos: 0, cis: 0}
max_tie = 0 #The highest number of passes between two players
max_cos = 0
max_cis = 0
#Compute Cos & Cis
with data as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        #If the player who made the pass is not in the dictionary, add it
        if(row[0] not in centrality_dict):
            centrality_dict[row[0]] = {"cos": int(row[2]), "cis": 0}
        #else update the cos value
        else:
            centrality_dict[row[0]]["cos"] = int(centrality_dict[row[0]]["cos"]) + int(row[2])
        
        #If the player who receive the pass is not in the dictionary, add it
        if(row[1] not in centrality_dict):
            centrality_dict[row[1]] = {"cos": 0, "cis": int(row[2])}
        #else update the cis value
        else:
            centrality_dict[row[1]]["cis"] = int(centrality_dict[row[1]]["cis"]) + int(row[2])
        if(max_cos < int(centrality_dict[row[0]]["cos"])):
                max_cos = int(centrality_dict[row[0]]["cos"])
        if(max_cis < int(centrality_dict[row[1]]["cis"])):
                max_cis = int(centrality_dict[row[1]]["cis"])
        # row variable is a list that represents a row in csv
        G.add_edge(row[0], row[1], weight=int(row[2]))
        total_passes = total_passes + int(row[2])
        if(int(row[2]) > max_tie):
            max_tie = int(row[2])
    

print("Total passes: ", total_passes)
network_intensity = total_passes #TODO: Normalize network intensity for team possession time or percentage of possession

data = open('./graphsNoSubs/Spain_Passes_Italy_Spain.csv', 'r')
next(data, None) #skip first line

#Compute the weight centralization
weight_centralization = 0
number_of_players = len(centrality_dict)
with data as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        weight_centralization = weight_centralization + max_tie - int(row[2])
weight_centralization = weight_centralization / ((number_of_players * (number_of_players - 1) -1) * total_passes)
print("Weight centralization: ", weight_centralization)
print("Number of players: ", number_of_players)

#Compute CI & CO
Ci = 0 # is highest when one player receives all passes and lowest when every member of the team receives an equal number of passes
Co = 0 # highest when one player makes all the passes and lowest when every member of the team makes the same number of passes.
print(max_cis)
print(max_cos)
for player in centrality_dict:
    Ci = Ci + (max_cis - centrality_dict[player]["cis"])
    Co = Co + (max_cos - centrality_dict[player]["cos"])
Ci = Ci / ((number_of_players - 1) * total_passes)
Co = Co / ((number_of_players -1) * total_passes)

print("Ci: ", Ci)
print("Co: ", Co)
'''
#la coppia di giocatori che si è passata la palla per più di 15 volte
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 8]
#i la coppia di giocatori che si è passata la palla per meno o uguale alle 15 volte
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 8]
pos = nx.spring_layout(G, seed=7) #inserire le posizioni dei giocatori


# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)
# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, edge_color="r")
nx.draw_networkx_edges(G, pos, edgelist=esmall, alpha=0.3, width=1, edge_color="b")


# node labels
#nx.draw_networkx_labels(G, pos, font_size=4, font_family="sans-serif")
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)


ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
#plt.show()
'''