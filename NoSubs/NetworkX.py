import networkx as nx
import matplotlib.pyplot as plt
data = open("./graphsNoSubs/Spain_Passes_Italy_Spain.csv","r")
next(data, None) #skip first line (column names)
graphType = nx.Graph()
graph = nx.parse_edgelist(data, delimiter = ",", create_using=graphType, data = (('weight', int),)) #missing nodetype

centrality = nx.degree_centrality(graph)
#out_centrality = nx.out_degree_centrality(graph)
#in_centrality = nx.in_degree_centrality(graph)
print(centrality)
#print(out_centrality)
#print(in_centrality)
centrality = nx.degree_centrality(graph)
nx.draw(graph, with_labels=True)
plt.show()
