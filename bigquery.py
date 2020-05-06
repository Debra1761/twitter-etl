import os
import tweepy
from google.cloud.bigquery.client import Client
from google.cloud import bigquery
from datetime import date, datetime
consumer_key = "jjSz1RE4ftTNmqB1XuUTM22Fc"
consumer_secret = "5SNWrhQStzMp3UDwVY7YGuEofQ4QOBBP4rOo4hGnhKpdFQoVi9"
access_token = "68979886-IzdibLmYAx39y8PLNWA7kLPKl2rTDlLPCnf557I45"
access_token_secret = "tjVsF4mx4vS9JO0hPcS7b8qoP7oIZK1A8nX0aMwhkNEDG"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))




os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api_key.json'
client = bigquery.Client()
dataset_id = 'Twitter_streams'
dataset_ref = client.dataset(dataset_id)
job_config = bigquery.LoadJobConfig()
job_config.schema = [
    bigquery.SchemaField ("user_id", "INT64"),
    bigquery.SchemaField ("created_at", "TIMESTAMP"),
    bigquery.SchemaField ("user_screen_name","STRING"),
    bigquery.SchemaField ("retweet_count", "NUMERIC"),
    bigquery.SchemaField ("id", "INT64"),
    bigquery.SchemaField ("text", "STRING"),
]



class MyStreamListener(tweepy.StreamListener):
  def on_status(self, status):
    tweet_json = {}
    tweet = ''
    # print(status.user)
    # print("user id: {}".format(status.user.id))
    # print("user screen name: {}".format(status.user.screen_name))
    # print("ID: {}".format(status.id))
    # print('truncated:', status.truncated)
    # print(status.created_at)
    # print(status.retweet_count)
    # print("\n")
    if hasattr(status, 'retweeted_status'):
      try:
        tweet = status.retweeted_status.extended_tweet["full_text"]
      except:
        tweet = status.retweeted_status.text
    else:
      try:
        tweet = status.extended_tweet["full_text"]
      except AttributeError:
        tweet = status.text
    # print(tweet)
    tweet_json['user_id'] = int(status.user.id)
    tweet_json['user_screen_name']=status.user.screen_name
    tweet_json['created_at'] = json_serial(status.created_at)
    tweet_json['id'] = int(status.id)
    tweet_json['retweet_count'] = status.retweet_count
    tweet_json['text'] = tweet
    # print('tweet json: ', tweet_json)
    tweet_json = [tweet_json]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    load_job = client.load_table_from_json(
    tweet_json,
    dataset_ref.table("twitter_table"),
    location="US",  # Location must match that of the destination dataset.
    job_config=job_config,
        )  # API request
    print("Starting job {}".format(load_job.job_id))
    load_job.result()  # Waits for table load to complete.
    print("Job finished.")
    print(load_job.result())




myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener , tweet_mode='extended', lang="en")
myStream.filter(track=["tesla", "teslamotors", "elon musk", "Tesla"])