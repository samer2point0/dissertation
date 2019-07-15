import networkx as nx
import random
import queue

def snow(g, seed=None, maxsize=30):
    """this function returns a set of nodes equal to maxsize from g that are
    collected from around seed node via snownball sampling"""
    if seed==None:
        seed=random.choice(list(g.nodes))
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

def mhda(g, seed=None, maxsize=30): #nonweighted and undirected edges
    if seed==None:
        seed=random.choice(list(g.nodes))
    if g.number_of_nodes() < maxsize:
        return set()
    current=seed
    prev=None
    subgraph = set(current)
    while len(subgraph) <= maxsize:
        neigh=list(g.neighbors(current))
        temp1=random.choice(neigh)
        p=random.random()
        if(p<=min(1,g.degree(current)/g.degree(temp1))):
            #move to another node if prob>thresh otherwise stay in place (no change to current and prev)
            if temp1==prev:
                #try again befor accepting (delay acceptance)
                if(len(neigh)==1): #if node has only one neighbor which it came from backtrack
                    temp=prev
                    prev=current
                    current=temp
                    subgraph.add(current)
                    continue
                neigh.remove(prev)
                temp2=random.choice(neigh)
                q=random.random()
                if q<=min(1,pow(min(1,g.degree(current)/g.degree(temp2))*max(1,g.degree(temp1)/g.degree(current)),2)):
                    #reject backtracking
                    prev=current
                    current=temp2
                else: #backtrack
                    prev=current
                    current=temp1
            else:
                #no backtrack so just move
                prev=current
                current=temp1
        subgraph.add(current)
    return subgraph
