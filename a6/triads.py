#!/usr/bin/env python
# coding: utf-8

# # CS581 A6 -- Triads in Epinions Data

# *Khayyam Saleem, Brendan Von Hofe*

# In[3]:


import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations as comb
from pprint import pprint
import pandas as pd


def graph_and_stats(fname):
    G = nx.Graph()
    self_loop_count = 0
    pos_count = 0
    neg_count = 0
    with open(fname, "r") as f:
        for line in f:
            reviewer, reviewee, weight = tuple(map(int, line.split(",")))
            self_loop_count += 1 if reviewer == reviewee else 0
            pos_count += 1 if weight == 1 and reviewer != reviewee else 0
            neg_count += 1 if weight == -1 and reviewer != reviewee else 0
            G.add_edge(reviewer, reviewee, weight=weight)
    return self_loop_count, pos_count, neg_count, G

self_loop_count, pos_count, neg_count, G = graph_and_stats("epinions_small.csv")


# In[2]:


weights = nx.get_edge_attributes(G, 'weight')


# In[3]:


triads = [x for x in nx.enumerate_all_cliques(G) if len(x) == 3]


# In[4]:


triads_and_weights = list(map(lambda x: list(map(lambda x: (x, weights[x]), comb(x, 2))), triads))


# In[5]:


from pprint import pprint
pprint(triads_and_weights[:20]) #ABBREVIATED


# In[58]:


print("NUMBER OF SELF LOOPS:", self_loop_count)
print("NUMBER OF TOTNODES:", pos_count+neg_count-self_loop_count)
print("NUMBER OF TRUST EDGES:", pos_count)
print("NUMBER OF DISTRUST EDGES:", neg_count)
print("NUMBER OF NODES IN TRIADS:",len(set([val for sublist in triads for val in sublist])))
print("NUMBER OF NODES TOTAL:",len(G.nodes()))


# **NUMBER OF SELF LOOPS:** 73  
# **NUMBER OF TOTNODES:** 65916  
# **NUMBER OF TRUST EDGES:** 57010  
# **NUMBER OF DISTRUST EDGES:** 8979  
# **NUMBER OF NODES IN TRIADS:** 3587  
# **NUMBER OF NODES TOTAL:** 10386

# In[12]:


def get_trust_category(entry):
    categories = {
        (1,1,1) : "TTT",
        (-1,1,1) : "TTD",
        (-1,-1,1) : "TDD",
        (-1,-1,-1) : "DDD"
    }
    return categories[tuple(sorted([x[1] for x in entry]))]

for i in range(len(triads_and_weights)):
    triads_and_weights[i].append(get_trust_category(triads_and_weights[i]))


# In[13]:


col_format = tuple(zip(*triads_and_weights))
table = pd.DataFrame({
    "trust_category": col_format[3],
    "edge_1": tuple(zip(*col_format[0]))[0],
    "trust_1": tuple(zip(*col_format[0]))[1],
    "edge_2": tuple(zip(*col_format[1]))[0],
    "trust_2": tuple(zip(*col_format[1]))[1],
    "edge_3": tuple(zip(*col_format[2]))[0],
    "trust_3": tuple(zip(*col_format[2]))[1]
})


# In[14]:


triad_table = table.sort_values(['trust_category'],ascending=False).reset_index(drop=True)


# In[21]:


triad_table.trust_category.unique()

with pd.option_context('display.max_columns', None):
    print(triad_table)


# In[16]:


num_edges = pos_count + neg_count
p_pos = pos_count / num_edges
p_neg = 1 - p_pos
p_type_1 = p_pos * p_pos * p_pos
p_type_2 = 3 * (p_pos * p_pos * p_neg)
p_type_3 = 3 * (p_pos * p_neg * p_neg)
p_type_4 = p_neg * p_neg * p_neg


# In[17]:


print("PROBABILITY THAT AN EDGE WILL BE POSITIVE:", p_pos)
print("PROBABILITY THAT AN EDGE WILL BE NEGATIVE:", p_neg)


# ### PROBABILITY THAT AN EDGE WILL BE POSITIVE: 
# *0.8639318674324509*
# ### PROBABILITY THAT AN EDGE WILL BE NEGATIVE:
# *0.13606813256754913*

# In[47]:


print("Expected distribution of TTT, TTD, TDD, and DDD triads are:\n{}, {}, {}, and {}. ".format(*list("n={0}: p={1:.2f}%".format(i, x*100) for i,x in zip((    len(triad_table[triad_table['trust_category']=='TTT']),    len(triad_table[triad_table['trust_category']=='TTD']),    len(triad_table[triad_table['trust_category']=='TDD']),    len(triad_table[triad_table['trust_category']=='DDD'])),(p_type_1,p_type_2,p_type_3,p_type_4)))))


# ### Expected distribution of TTT, TTD, TDD, and DDD triads are:
# *n=159876: p=64.48%, n=33443: p=30.47%, n=21292: p=4.80%, and n=3385: p=0.25%.*

# In[19]:


n_triads = len(triad_table)
type_1 = len(triad_table[triad_table['trust_category'] == 'TTT'])
type_2 = len(triad_table[triad_table['trust_category'] == 'TTD'])
type_3 = len(triad_table[triad_table['trust_category'] == 'TDD'])
type_4 = len(triad_table[triad_table['trust_category'] == 'DDD'])


# In[52]:


print("Actual distribution of TTT, TTD, TDD, and DDD triads are respectively {0:.2f}%, {1:.2f}%, {2:.2f}%, and {3:.2f}%.".format(*list(map(lambda x: x*100, (type_1 / n_triads, type_2 / n_triads, type_3 / n_triads, type_4 / n_triads)))))


# ### Actual distribution of TTT, TTD, TDD, and DDD triads are respectively:
# *73.34%, 15.34%, 9.77%, and 1.55%.*
# 

# ## EXTRA

# A minimum spanning tree is the minimal set of edges that yields a connected subgraph on the same nodeset as the original graph. In this context, it shows how people may travel from one reviewer to another based on trust. Users are more likely to meet other reviewers through entities that they trust. However, since the original graph was not connected, a spanning tree does not exist. Rather, a spanning forest exists. Hence, some reviewers are unlikely to meet others at all without the intervention of some third-party adding edges or abnormal behavior.

# In[4]:


print("NUMBER OF EDGES IN MINIMUM SPANNING TREE:", len(nx.minimum_spanning_tree(G).edges())) #edge size of minimum spanning tree


# In[6]:


print("NUMBER OF EDGES IN ORIGINAL GRAPH:",len(G.edges())) # number of edges in original graph


# In[ ]:




