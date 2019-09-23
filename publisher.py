import config
import tweepy

from twitter_stream import TwitterStreamListener

def publish_twitter_stream():
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    stream_listener = TwitterStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['😡'])

if __name__ == '__main__':
    publish_twitter_stream()