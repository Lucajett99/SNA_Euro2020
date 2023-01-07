import networkx as nx
import matplotlib.pyplot as plt
import statistics
import csv
import os 

def mean(dict):
    sum = 0
    for val in dict.values():
        sum += val
    mean =  sum / len(dict)
    return str(sum)


total_centrality = {}
squadName = "Italy"
for file in os.listdir("./graphsNoSubs/"):
    if file.startswith(squadName):
        print(file)
        data = open('./graphsNoSubs/' + file, 'r', encoding='utf-8')
        next(data, None) #skip first line
        total_passes = 0
        G = nx.DiGraph()    

        with data as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = csv.reader(read_obj)
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

        centrality = G.in_degree(weight='weight')
        weighted_centrality = {}
        for player in centrality:
            weighted_centrality[player[0]] = player[1] / total_passes
            
            if(player[0] not in total_centrality):
                total_centrality[player[0]] = weighted_centrality[player[0]]
            else:
                total_centrality[player[0]] += weighted_centrality[player[0]]
        
        print(sorted(weighted_centrality.items(), key=lambda x:x[1]))
        print("Max: " + max(weighted_centrality, key=weighted_centrality.get))
        print("Mean: " + mean(weighted_centrality) + "\n\n")
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
print("TOTALI\n")
print(sorted(total_centrality.items(), key=lambda x:x[1]))
print("Total Max: " + max(total_centrality, key=total_centrality.get))
print("Total Mean: " + mean(total_centrality) + "\n\n")

#Modric Mean: 0,153632232365031125
#Kovavic Mean: 0,12402384710603185

