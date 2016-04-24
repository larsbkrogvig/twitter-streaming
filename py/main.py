import os
import ConfigParser
import tweepy


def get_local_config():
    """Load Twitter API credentials from ~/.credentials/twitter."""

    config = ConfigParser.ConfigParser()
    config.read('%s/.credentials/twitter' % os.environ['HOME'])

    return config


def main():

    config = get_local_config()

    auth = tweepy.OAuthHandler(
        config.get('OAuth', 'consumer_key'),
        config.get('OAuth', 'consumer_secret')
    )

    # auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print tweet.text

    pass


if __name__ == '__main__':
    main()
