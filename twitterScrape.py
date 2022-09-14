import snscrape.modules.twitter as sntwitter
import pandas as pd
import json
# Created a list to append all tweet attributes(data)
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('COVID Vaccine since:2021-01-01 until:2021-05-31').get_items()):
    if i>5000:
        break
    attributes_container.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
# Creating a dataframe from the tweets list above 
tweets_df = pd.DataFrame(attributes_container, columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])
#print(tweets_df.to_string())
result = tweets_df.to_json('temp.json',orient="records")
parsed = json.loads(result)
json.dumps(parsed, indent=4)

