import networkx as nx
import sampling
import concept
import algor
import numpy
import copy
import pandas as pd
import itertools



def prop(g):
    print('number of nodes', g.number_of_nodes())
    print('no of edges ', g.size())
    print('graph has ', nx.number_connected_components(g), 'connected component')
