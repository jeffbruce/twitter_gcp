import config
import tweepy

class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print(status.text)
        print(status.user.location)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth, wait_on_rate_limit=True)
api = tweepy.API(auth)

stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['😡'])
