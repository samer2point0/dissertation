import networkx as nx
import matplotlib.pyplot as plt
import random
import queue

def snowball(g, seed, maxsize=20):
    """this function returns a set of nodes equal to maxsize from g that are
    collected from around seed node via snownball sampling"""
    if g.number_of_nodes() < maxsize:
        return set()
    q = queue.Queue()
    q.put(seed)
    subgraph = set(seed)
    while not q.empty():
        for node in g.neighbors(q.get()):
            if len(subgraph) < maxsize:
                q.put(node)
                subgraph.add(node)
            else :
                return subgraph
    return subgraph

def mhla(g, seed, steps=20):
    G=nx.Graph()
    G.add_node(seed)
    new=seed
    for i in range(0,20):
        neighbors=G.neighbors(new)
        temp=random.choice(neighbors) #all edges are equally liekly (no weight on edges)



f=open('gr.txt', 'rb')
G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
f.close()
seed=random.choice(list(G.nodes))
#sn=snowball(G,seed)
#snowballG=G.subgraph(sn)

sG=mhla(G,seed)
print(sG.nodes)
nx.draw(sG, with_labels=True)
plt.show()
