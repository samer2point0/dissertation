import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import sampling
import concept
import algor
import numpy
import copy



def present(g, sub, col=['#dbb844'],pos=None):
    #takes graph, list of sub node lists, and list of colors
    if pos==None:
        pos=nx.spring_layout(g)
    dcol='#668aae'
    nL=[x for x in g.nodes() if not x in sub]
    cL=[dcol]*len(nL)
    for i in range(0,len(sub)):
        nL.extend(sub[i])
        cL.extend([col[i]]*len(sub[i]))
    nx.draw(g, nodelist=nL, node_color=cL, with_labels=False, pos=pos)
    plt.show()
