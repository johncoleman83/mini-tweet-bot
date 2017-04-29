"""
app module
takes user input and tweets to designated account
"""
import web
import tweepy
from credentials import *
import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

urls = (
    '/', 'index',
    '/confirmtweet', 'confirmtweet',
    '/features', 'features',
    '/confirmfeature', 'confirmfeature'
)
app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")

def tweet_text(tweetvar):
    """ tweets text from input variable """
    if tweetvar != '\n':
        api.update_status(tweetvar)

def auto_tweet():
    """ runs for loop through all lines read in text file """
    my_file = open('test.txt', 'r')
    file_lines = my_file.readlines()
    my_file.close()
    for line in file_lines:
        if line != '\n':
            api.update_status(line)
            sleep(30)
        else:
            pass

def follow_followers():
    """ follow all your followers """
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

def follow_ten(searchterms):
    """follow ten new followers based on given searchterms"""
    for tweet in tweepy.Cursor(api.search, q=searchterms).items(10):
        try:
            if not tweet.user.following:
                tweet.user.follow()
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def retweet_follow(searchterms):
    """primary function that runs for loop"""
    for tweet in tweepy.Cursor(api.search, q=searchterms).items():
        try:
            tweet.retweet()
            if not tweet.user.following:
                tweet.user.follow()
                break
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

class index(object):
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input()
        try:
            tweetvar = "%s" % (form.tweet)
            tweet_text(tweetvar)
            return render.confirmtweet(tweetvar = tweetvar)
        except:
            return render.confirmtweet(tweetvar = "")

class confirmtweet:
    def GET(self):
        return render.confirmtweet(tweetvar = "")

class features:
    def GET(self):
        return render.features()

    def POST(self):
        form = web.input()
        try:
            retweet = "%s" % (form.retweet)
            if form.searchterms:
                searchterms = "%s" % (form.searchterms)
                retweet_follow(searchterms)
            else:
                retweet_follow("#diversity")
        except:
            pass
        try:
            if form.followthem:
                follow_followers()
        except:
            pass
        try:
            if form.followten:
                if form.searchterms:
                    searchterms = "%s" % (form.searchterms)
                    follow_ten(searchterms)
                else:
                    follow_ten("#opensource")
        except:
            pass
        try:
            if form.autotweet:
                auto_tweet()
        except:
            pass
        return render.confirmfeature(status = "success")

class confirmfeature:
    def GET(self):
        return render.confirmfeature(status = "")

if __name__ == "__main__":
    app.run()
