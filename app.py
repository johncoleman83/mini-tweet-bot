"""
app module
takes user input and tweets to designated account
"""
import web
import tweepy
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

urls = (
    '/', 'index',
    '/confirmtweet', 'confirmtweet'
)
app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")

def tweet_text(tweetvar):
    """ tweets text from input variable """
    if tweetvar != '\n':
        api.update_status(tweetvar)

class index(object):
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input(tweet="tweet")
        tweetvar = "%s" % (form.tweet)
        tweet_text(tweetvar)
        return render.confirmtweet(tweetvar = tweetvar)

class confirmtweet:
    def GET(self):
        tweetvar = "no tweet"
        return render.confirmtweet(tweetvar = tweetvar)

if __name__ == "__main__":
    app.run()
