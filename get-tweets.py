import tweepy

def stream_saver(search_terms):
    consumer_key = 'qBaFzrUpKKLfPHIj7E3DYASoZ'
    consumer_secret = 'mJnvR16V6YlTgXQbRxAK7anxk74jfplTNiHRbkH6R3gI8MIgfu'
    access_token = '941847418873745408-xK9YYfAWXa2xdXiPBmcuBSskq2DGDIZ'
    access_token_secret = 'BNt8ss4idIMVwpNJUnpdiYt6xhQaPIaftgjv0VtUP3gnc'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth)

    class CustomStreamListener(tweepy.StreamListener):

        def on_status(self, status):
            print (status.author.screen_name, status.created_at, status.text)

    streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener())
    streamingAPI.filter(track=[search_terms])
    
    
stream_saver('wow')
