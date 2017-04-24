"""
tweet_textfile module
in for loop, reads text from text file, and tweets it if it's new text
"""
import tweepy
from time import sleep
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

my_file = open('tweet.txt', 'r')
file_lines = my_file.readlines()
my_file.close()

def tweet_text():
""" runs for loop through all lines read in text file """
    for line in file_lines:
        if line != '\n':
            api.update_status(line)
            sleep(86400)
        else:
            pass

tweet_text()
