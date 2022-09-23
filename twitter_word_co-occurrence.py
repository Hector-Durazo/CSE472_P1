import re
import json
import nltk
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import snscrape.modules.twitter as sntwitter

#preproccessing tweets and removing stop words and punctuation
def drawGraph(G:nx.Graph) ->None:
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
    ax2.set_xlabel("Closeness")
    ax2.set_ylabel("# of Nodes")

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.hist(nx.pagerank(G).values(), bins=70)
    ax1.set_title("Page Ranking Histogram")
    ax1.set_ylabel("# of Nodes")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()

def tweetPreproccessing(json_load:json) -> None:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('words')

    #list of words to remove if they start with these chars
    sw_list = ['id','like','feel','im','likes','go','dont','us','theyre','got','going','#']
    rmv_list = ('@', '/', 'http', '#','1','2', '3', '4', '5', '6', '7', '8', '9', '0')

    all_stopwords = stopwords.words('english')
    all_stopwords.extend(sw_list)
    words = set(nltk.corpus.words.words())

    G = nx.Graph()
    numOfNode = 0
    x=0
    while numOfNode < 250:
        scentence = json_load[x]["Source of Tweet"]

        #removes links, twitter handles, and random words that start with numbers
        scentence = " ".join(
            filter(lambda word: not word.lower().startswith(rmv_list),
                   scentence.split()))

        #removed punctuation
        scentence = re.sub(r'[^\w\s]', '', scentence)

        #separates every word and removes all stop words
        text_tokens = word_tokenize(scentence.lower())
        tokens_without_sw = [
            word for word in text_tokens if not word in all_stopwords
        ]

        #checks for english words // not sure to add because removes some real english words // about 20k words are removed
        tokens_without_sw = [
            w for w in tokens_without_sw if w.lower() in words or not w.isalpha()
        ]

        for i in range(len(tokens_without_sw)-1):
            G.add_edge(tokens_without_sw[i], tokens_without_sw[i+1])
        numOfNode = G.number_of_nodes()
        x = x + 1
    
    #print("number of tweets: " + str(x))
    G.remove_edges_from(nx.selfloop_edges(G))
    drawGraph(G)

def tweetScraping(filter: str) -> None:

    attributes_container = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(filter).get_items()):
        if i > 300:
            break
        attributes_container.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(attributes_container,
                             columns=[
                                 "Date Created", "Number of Likes",
                                 "Source of Tweet", "Tweets"
                             ])
    tweets_df.to_json(filter + '.json', orient="records")

    with open(filter + '.json', 'r') as json_file:
        jsondata = json.load(json_file)

    tweetPreproccessing(jsondata)

tweetScraping('#VaccinesWork')
tweetScraping('#NoVaxMandates')