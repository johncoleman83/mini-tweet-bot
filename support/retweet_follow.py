"""
retweet_follow module
in for loop, finds tweet, retweets it and follows the user
"""
import tweepy
from time import sleep
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def retweet_follow():
    """primary function that runs for loop"""
for tweet in tweepy.Cursor(api.search, q='#opensource').items():
    try:
        tweet.retweet()
        if not tweet.user.following:
            tweet.user.follow()
        sleep(86400)
    except:
        print("error")
        break


retweet_follow()
