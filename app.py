"""
app module
takes user input and tweets to designated account
"""
import web
import tweepy
from credentials import *
from time import sleep

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
    api.update_status(tweetvar)

def auto_tweet(filename, seconds):
    """ runs for loop through all lines read in text file """
    fout = open(filename, 'r')
    file_lines = fout.readlines()
    fout.close()
    for line in file_lines:
        try:
            if line != '\n':
                api.update_status(line)
            else:
                pass
        except:
            pass
        sleep(seconds)

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
        form = web.input(inputfile={})
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
                if 'inputfile' in form:
                    filepath=form.inputfile.filename.replace('\\','/')
                    filename=filepath.split('/')[-1]
                    fout = open(filename, 'w')
                    fout.write(form.inputfile.file.read())
                    fout.close()
                    try:
                        seconds = form.seconds
                        auto_tweet(filename, seconds)
                    except:
                        auto_tweet(filename, 10800)
        except:
            pass
        return render.confirmfeature(status = "success")

class confirmfeature:
    def GET(self):
        return render.confirmfeature(status = "")

if __name__ == "__main__":
    app.run()
