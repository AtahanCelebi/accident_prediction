import tweepy
import pandas as pd
import datetime
# authorization tokens
consumer_key = "NEiYEJuAsTAyxy62mO2hBXqFE"

consumer_secret = "TUQseEIwoWyuRNiwlxiVTCl0qw4HxZreugNBuFTTJeH5ABcvcr"

access_token = "1007387591245815809-rgA92md4jDIdQ0jJ1QJkuvjlGa4Boz"
access_token_secret = "DNG5QYbYKWNkZKsjyBRnmKVZ3HRAyi7PeGpIjoEudUa3C"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

username = '4444154'
#Method - 1
count = 80
try:
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.user_timeline, id=username).items(15)
    # Pulling information from tweets iterable object
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
    print(tweets_df)
    print(len(tweets_df))
except BaseException as e:
    print('failed on_status,', str(e))

#Method - 2
startDate = datetime.datetime(2021, 4, 4,0,0)
endDate =   datetime.datetime(2021, 4, 8,23,59)
tweets2 = []
tmpTweets = api.user_timeline(username)
for i in tmpTweets:
    if i.created_at < endDate and i.created_at > startDate:
        tweets2.append(i.created_at)

while (tmpTweets[-1].created_at > startDate):
    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
    for j in tmpTweets:
        if j.created_at < endDate and j.created_at > startDate:
            tweets2.append(j.created_at)

for i in tweets2:
    print(i)