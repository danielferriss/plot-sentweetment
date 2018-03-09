import plotly
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np
import datetime
import time
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from langdetect import detect


stream_ids = tls.get_credentials_file()['stream_ids']

# Get stream id from stream id list 
stream_id = stream_ids[0]

# Make instance of stream id object 
stream = Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=100      # (!) keep a max of 80 pts on screen
)


# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='markers',
    text=[],
    stream=stream         # (!) embed stream id, 1 per trace
)

data = Data([trace1])

search_term = 'Microsoft'
# Add title to layout object
layout = Layout(title='Real Time Sentiment of Tweets About %s' %search_term)

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='2838838482839428349234928')

# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
s = py.Stream(stream_id)

# (@) Open the stream
s.open()

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)


#Secret Twitter Keys
# consumer_key = 'secret'
# consumer_secret = 'secret'
# access_token = 'secret'
# access_token_secret = 'secret'

consumer_key = 'qBaFzrUpKKLfPHIj7E3DYASoZ'
consumer_secret = 'mJnvR16V6YlTgXQbRxAK7anxk74jfplTNiHRbkH6R3gI8MIgfu'
access_token = '941847418873745408-xK9YYfAWXa2xdXiPBmcuBSskq2DGDIZ'
access_token_secret = 'BNt8ss4idIMVwpNJUnpdiYt6xhQaPIaftgjv0VtUP3gnc'

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
        #langdetect throws an error if the tweet is only a link or only emojis, or a mix of the two.
        #This stops that from happening
        try:
            if detect(tweet) == 'en':
                x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                y = sid.polarity_scores(tweet)['compound']
                # (@) write to Plotly stream!
                text = '%s:\n \"%s\"' %(author, tweet)
                s.write(dict(x=x, y=y, text=text))
        except:
            pass

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=[search_term])
s.close()
