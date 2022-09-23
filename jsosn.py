import json
import nltk
import re
import scipy as sp
import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

G = nx.Graph()

nltk.download('stopwords')
nltk.download('punkt')
all_stopwords = stopwords.words('english')
sw_list = ['id','like','feel','im','likes','go','dont',
            'us','theyre','got','going','#']
all_stopwords.extend(sw_list)

nltk.download('words')
words = set(nltk.corpus.words.words())


with open('temp.json', 'r') as json_file:
    json_load = json.load(json_file)

#list of words to remove if they start with these chars
rmv_list = ('@', '/', 'http', '#',
            '1','2', '3', '4', '5', '6', '7', '8', '9', '0')

#preproccessing tweets and removing stop words and punctuation
##still working on removeing @
for x in range(150):
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

    for i in range(len(tokens_without_sw)-1):
        G.add_edge(tokens_without_sw[i], tokens_without_sw[i+1])


G.remove_edges_from(nx.selfloop_edges(G))
print(G.number_of_nodes())


options = {
    'node_color': 'grey',
    'node_size': 10,
    'linewidths': 0,
    'width': 0.1,
    'font_size':5,
    #'with_labels':True
}
nx.draw(G, **options)


degree_sequence = sorted((d for n, d in nx.degree(G)), reverse=True)

fig= plt.figure("ProVAX", figsize=(8,8))
axgrid = fig.add_gridspec(5,4)

ax2 = fig.add_subplot(axgrid[0:3, :])
ax2.hist(nx.closeness_centrality(G).values(),bins=160)
ax2.set_title("Closeness Centrality Histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.hist(nx.pagerank(G).values(), bins=70)
ax1.set_title("Pageranking Histogram")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*sp.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.show()
