import os
import ConfigParser
import tweepy
import time
import json


class StandardListener(tweepy.StreamListener):
    """Listens to stream and prints everything"""

    def on_data(self, data):
        tweet = json.loads(data)
        print_tweet(tweet)

    def on_error(self, status):
        print status
        return False # Returning False stops streaming


def local_config():
    """Load Twitter API credentials from ~/.credentials/twitter."""

    config = ConfigParser.ConfigParser()
    config.read('%s/.credentials/twitter' % os.environ['HOME'])

    return config


def twitter_authentication(config):
    """Authenticate with Twitter using credentials in config."""

    auth = tweepy.OAuthHandler(
        config.get('OAuth', 'consumer_key'),
        config.get('OAuth', 'consumer_secret')
    )
    auth.set_access_token(
        config.get('OAuth', 'access_token'),
        config.get('OAuth', 'access_token_secret')
    )

    return auth


def start_listening(stream, filter=None, simulate=True):
    """Starts streaming and applies listener.
    Uses sample tweets from file instead of streaming API if simulate=True"""

    if filter:
        assert type(filter) is list, "filter must be a list"

    if simulate:

        if filter:
            print ('Warning: Simulated streaming turned on, '
                   'filters [%s] are ignored') % ','.join(filter)

        # Simulate streaming with sample tweets
        with open('resources/sample_tweets.txt', 'r') as f:
            lines = f.read().splitlines()

            for l in lines:
                stream.listener.on_data(l)
                time.sleep(0.1)

    else:
        # Listen to actual stream
        stream.filter(track=filter)


def print_tweet(tweet):

    header = '%s - %s' % (tweet['user']['name'], tweet['created_at'])
    body = '%s\n' % tweet['text']
    width = min(140, max(len(header), len(body)))

    print header
    print '#' * width
    print '%s' % tweet['text']
    print '#' * width, '\n' * 2


def main():

    config = local_config()
    auth = twitter_authentication(config)
    listener = StandardListener()
    stream = tweepy.Stream(auth, listener)

    start_listening(stream, ['chess'])

    pass


if __name__ == '__main__':
    main()
