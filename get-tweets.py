import tweepy
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

#Secret Twitter Keys
consumer_key = 'secret'
consumer_secret = 'secret'
access_token = 'secret'
access_token_secret = 'secret'



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#sentiment analysis
sid = SIA()

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweet = status.text
        author = status.author.screen_name
        sentiment = sid.polarity_scores(tweet)

        print(author, '\n', tweet, '\n', sentiment, '\n\n')

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=['microsoft'])