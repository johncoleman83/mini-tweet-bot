"""
singlefunction
this is a file with a single function that shows an example of how to execute
the twitter integration functions without using the web user interface web.py
nor any of its integrations is needed.
"""
import tweepy
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet_text(tweetvar):
    """ tweets text from input variable """
    try:
        api.update_status(tweetvar)
    except:
        print("error")
        pass


tweet_text("this tweet is an example of running a tweet function in python")
