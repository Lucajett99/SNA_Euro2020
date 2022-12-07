import networkx as nx
import matplotlib.pyplot as plt
from csv import reader
''''
data = open("./graphsNoSubs/Spain_Passes_Italy_Spain.csv","r")
next(data, None) #skip first line (column names)

graphType = nx.Graph()
graph = nx.parse_edgelist(data, delimiter = ",", create_using=graphType, data = (('weight', int),)) #missing nodetype

centrality = nx.degree_centrality(graph)
closness_centrality = nx.closeness_centrality(graph)
#out_centrality = nx.out_degree_centrality(graph)
#in_centrality = nx.in_degree_centrality(graph)
print(centrality)
print(closness_centrality)
#print(out_centrality)
#print(in_centrality)
centrality = nx.degree_centrality(graph)
nx.draw(graph, with_labels=True)
plt.show()
'''

G = nx.DiGraph()
data = open('./graphsNoSubs/Spain_Passes_Italy_Spain.csv', 'r')
next(data, None) #skip first line
total_passes = 0

with data as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        G.add_edge(row[0], row[1], weight=int(row[2]))
        total_passes = total_passes + int(row[2])


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

centrality = G.degree(weight='weight')
weighted_centrality = {}
for player in centrality:
    weighted_centrality[player[0]] = player[1] / total_passes

print(max(weighted_centrality.values()))
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
