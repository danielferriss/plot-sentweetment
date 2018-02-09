import tweepy
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from langdetect import detect

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

#enter search word in console
search_term = input("Enter what word you would like to search for: ")

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweet = status.text
        #langdetect throws an error if the tweet is only a link or only emojis, or a mix of the two.
        #This stops that from happening
        try:
            if detect(tweet) == 'en':
                author = status.author.screen_name
                sentiment = sid.polarity_scores(tweet)
                print(author, '\n', tweet, '\n', sentiment, '\n\n')
        except:
        	pass

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=[search_term])