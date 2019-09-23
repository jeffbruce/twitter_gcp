import base64
import json
import time

from google.cloud import bigquery
from google.cloud import pubsub_v1

import config

def write_tweets_to_bq(dataset_id, table_id, tweets):
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    errors = client.insert_rows(table, tweets)
    if not errors:
        print('Loaded {} row(s) into {}:{}'.format(len(tweets), dataset_id, table_id))
    else:
        print('Errors:')
        for error in errors:
            print(error)

def collect_tweets(data):
    tweets = []
    stream = base64.urlsafe_b64decode(data)
    twraw = json.loads(stream)
    twmessages = twraw.get('messages')
    for message in twmessages:
        tweets.append(message['data'])

    write_tweets_to_bq(config.BIGQUERY_DATASET_ID, config.BIGQUERY_TABLE_ID, tweets)

def receive_tweets(project, subscription_name):
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        collect_tweets(message.data)
        message.ack()

    subscription = client.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))

    # future = subscription.open(callback)
    # try:
    #     future.result()
    # except Exception as e:
    #     print('Listening for messages on {} threw an Exception: {}'.format(subscription_name, e))
    #     raise

    while True:
        time.sleep(60)

if __name__ == '__main__':
    receive_tweets(config.GCP_PROJECT, config.GCP_SUBSCRIPTION)

