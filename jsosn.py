import json
from optparse import Option
import nltk
import numpy as np
import collections
import re
import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

G = nx.Graph()

total = 0

nltk.download('stopwords')
nltk.download('punkt')
all_stopwords = stopwords.words('english')
sw_list = [
    'id',
    'like',
    'feel',
    'im',
    'likes',
    'go',
    'dont',
    'us',
    'theyre',
    'got',
    'going',
    '#',
]
all_stopwords.extend(sw_list)

nltk.download('words')
words = set(nltk.corpus.words.words())

with open('temp.json', 'r') as json_file:
    json_load = json.load(json_file)

#list of words to remove if they start with these chars
rmv_list = ('@', '/', 'http', '#'
            '1', '3', '4', '5', '6', '7', '8', '9', '0')
#preproccessing tweets and removing stop words and punctuation
##still working on removeing @
for x in range(30):
    text = json_load[x]["Source of Tweet"]

    #removes links, twitter handles, and random words that start with numbers
    result = " ".join(
        filter(lambda word: not word.lower().startswith(rmv_list),
               text.split()))

    #removed punctuation
    result = re.sub(r'[^\w\s]', '', result)

    #separates every word and removes all stop words
    text_tokens = word_tokenize(result.lower())
    tokens_without_sw = [
        word for word in text_tokens if not word in all_stopwords
    ]

    #checks for english words // not sure to add because removes some real english words // about 20k words are removed
    tokens_without_sw = [
        w for w in tokens_without_sw if w.lower() in words or not w.isalpha()
    ]
    for i in tokens_without_sw:
        for j in tokens_without_sw:
            G.add_edge(i, j)
G.remove_edges_from(nx.selfloop_edges(G))
print(G.number_of_nodes())

# print degree for each team - number of games
#for n, d in G.degree():
#    print('%s %d' % (n, d))
#
#options = {
#    'node_color': 'black',
#    'node_size': 50,
#    'linewidths': 0,
#    'width': 0.1,
#}
#nx.draw(G, **options)
#plt.show()

deg_centrality = nx.degree_centrality(G)
centrality = np.fromiter(deg_centrality.values(), float)
# plot
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, node_color=centrality, node_size=centrality*2e3)
nx.draw_networkx_labels(G, pos)
plt.show()
