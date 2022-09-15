import json
from optparse import Option
import nltk
import re
import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
G = nx.Graph()


total =0

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
    'dont'
    '#'
]
all_stopwords.extend(sw_list)

nltk.download('words')
words = set(nltk.corpus.words.words())

with open('temp.json', 'r') as json_file:
    json_load = json.load(json_file)

#list of words to remove if they start with these chars
rmv_list = ('@', '/', 'http','#' '1', '3', '4', '5', '6', '7', '8', '9', '0')
#preproccessing tweets and removing stop words and punctuation
##still working on removeing @
for x in range(1):
    text = json_load[x]["Source of Tweet"]

    #removes links, twitter handles, and random words that start with numbers
    result = " ".join(
        filter(lambda word: not word.lower().startswith(rmv_list),
               text.split()))

    #removed punctuation
    result = re.sub(r'[^\w\s]','',result)

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
            G.add_edge(i,j)
G.remove_edges_from(nx.selfloop_edges(G))
print(G.number_of_nodes())

options = {
    "font_size": 6,
    "node_size": 700,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
}
nx.draw_networkx(G,**options)

ax = plt.gca()
ax.margins(0.10)
plt.axis("off")
plt.show()
print(G.number_of_nodes())
#total=total + len(tokens_without_sw)
#print(total)
#print(tokens_without_sw)
