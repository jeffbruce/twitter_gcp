import base64
import json

from google.cloud import pubsub_v1
from tweepy import StreamListener

import config

def publish(client, topic_path, data_lines):
    messages = []
    for line in data_lines:
        messages.append({'data': line})
    body = {'messages': messages}
    str_body = json.dumps(body)
    data = base64.urlsafe_b64encode(bytearray(str_body, 'utf8'))
    client.publish(topic_path, data=data)

class TwitterStreamListener(StreamListener):
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(config.GCP_PROJECT, config.GCP_TOPIC)
    count = 0
    tweets = []
    batch_size = 50
    total_tweets = 1000

    def on_status(self, status):
        print(' '.join(['Processing:\n', status.text]))
        
        tweet_id = status.id
        text = status.text
        retweets = status.retweet_count
        location = status.user.location
        tweet = dict(id=tweet_id, text=text, retweets=retweets, location=location)

        self.tweets.append(tweet)
        if len(self.tweets) >= self.batch_size:
            publish(self.client, self.topic_path, self.tweets)
            self.tweets = []

        self.count += 1
        if (self.count % 50) == 0:
            print("count is {}".format(self.count))
        if self.count >= self.total_tweets:
            return False

        return True

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnect the stream.
            return False
