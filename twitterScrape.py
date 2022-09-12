import snscrape.modules.twitter as sntwitter
import pandas as pd
import json
# Created a list to append all tweet attributes(data)
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:Gallandivater').get_items()):
    attributes_container.append([tweet.follower, tweet.likeCount, tweet.sourceLabel, tweet.content])
    #print(tweet.date,tweet.likeCount, tweet.content)
# Creating a dataframe from the tweets list above 
tweets_df = pd.DataFrame(attributes_container, columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])
#print(tweets_df.to_string())
result = tweets_df.to_json('temp.json',orient="records")
parsed = json.loads(result)
json.dumps(parsed, indent=4)