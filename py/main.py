# -*- coding: utf-8 -*-
# python 2

import os
import ConfigParser
import tweepy
import time
import json
import re
from collections import Counter


common_words = [
    'https'
]


class StandardListener(tweepy.StreamListener):
    """Listens to stream and prints everything"""

    def on_data(self, data):
        tweet = json.loads(data)
        print_tweet(tweet)

    def on_error(self, status):
        print status
        return False # Returning False stops streaming

class WordCountListener(tweepy.StreamListener):
    """Listens to stream and prints everything"""

    def __init__(self):
        self.counter = Counter()

    def on_data(self, data):

        tweet = json.loads(data)

        if tweet['lang'] == 'en':
            text = tweet['text']
            words = map(lambda x: x.lower(), re.findall('\w+', text))

            for word in words:
                if len(word) >= 4 and word not in common_words:
                    self.counter[word] += 1

            print_tweet(tweet)
            print self.counter.most_common(10)

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
    """Prints a json tweet in a human-readable format"""

    header = '%s - %s' % (tweet['user']['name'], tweet['created_at'])
    body = '%s\n' % tweet['text']
    width = min(140, max(len(header), len(body)))

    print header, '(%s)' % tweet['lang']
    print '#' * width
    print '%s' % tweet['text']
    print '#' * width, '\n' * 2


#def detect_squares(text, moves):
#
#    words #= map(lambda x: x.lower(), re.findall('\w+', text))
#
#    squares = [(i, '%s%i' % (w[0], len(w)))
#               for i, w in enumerate(words)
#               if w[0] in 'abcdefgh' and len[w] <= 8]
#
#    return squares


def pick_move(text, moves):
    return moves[hash(text) % len(moves)]


def main():

    config = local_config()
    auth = twitter_authentication(config)
    listener = WordCountListener()
    stream = tweepy.Stream(auth, listener)

    start_listening(stream, ['pizza'], simulate=False)

    pass


if __name__ == '__main__':
    main()
