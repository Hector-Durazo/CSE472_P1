import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(
            'lang:en since:2022-09-07').get_items()):
    if i > 100:
        break
    tweets_list2.append(
        [tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2,
                          columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
print(tweets_df2)
tweets_df2.to_json('temp.json', orient="index", force_ascii=True)
