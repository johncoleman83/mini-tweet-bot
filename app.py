"""
app python mini tweet bot application
takes user input and tweets to designated account
"""
import web
import tweepy
import multiprocessing
from time import sleep
from credentials import *

# censoring functions
import censorship

# dictionaries
from aldict import ascii_dict
from aldict import leet_dict

# import functions
remove_whitespace = censorship.remove_whitespace
censor = censorship.censor

# tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# web.py
urls = (
    '/', 'index',
    '/confirmtweet', 'confirmtweet',
    '/features', 'features',
    '/confirmfeature', 'confirmfeature'
)
app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")

# translation to ascii or leet


def translate(tweetvar, c):
    if c == 'a':
        tweetvar = tweetvar.lower()
        for key in ascii_dict:
            if key in tweetvar:
                tweetvar = tweetvar.replace(key, ascii_dict[key])
    else:
        for key in leet_dict:
            if key in tweetvar:
                tweetvar = tweetvar.replace(key, leet_dict[key])
    return tweetvar


# begin tweet functions here


def tweet_text(tweetvar):
    """ tweets text from input variable """
    try:
        api.update_status(tweetvar)
    except:
        return False
    return True


def retweet_follow(searchterms):
    """searches tweets with searchterms, retweets, then follows"""
    for tweet in tweepy.Cursor(api.search, q=searchterms).items(60):
        try:
            tweet.retweet()
            if not tweet.user.following:
                tweet.user.follow()
            return True
        except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False


def follow_x(searchterms, xfollowers):
    """follow ten new followers based on given searchterms"""
    retval = False
    for x in range(xfollowers):
        for tweet in tweepy.Cursor(api.search, q=searchterms).items(60):
            try:
                if not tweet.user.following:
                    tweet.user.follow()
                    retval = True
                    break
            except tweepy.TweepError as e:
                print(e.reason)
                pass
    return retval


def auto_retweet(searchterms, seconds, iterations):
    """ searches for tweets, attempts to retweet, follows, and repeat """
    for x in range(iterations):
        for tweet in tweepy.Cursor(api.search, q=searchterms).items(60):
            try:
                tweet.retweet()
                if not tweet.user.following:
                    tweet.user.follow()
                break
            except tweepy.TweepError as e:
                print(e.reason)
                pass
        sleep(seconds)


def auto_tweet_file(filename, seconds):
    """ runs loop through all lines in text file and tweets them """
    fout = open(filename, 'r')
    file_lines = fout.readlines()
    fout.close()
    for line in file_lines:
        try:
            if line != '\n':
                if censor(line):
                    api.update_status(line)
            else:
                pass
        except tweepy.TweepError as e:
            print(e.reason)
            pass
        sleep(seconds)


def follow_followers():
    """ follow all your followers """
    for follower in tweepy.Cursor(api.followers).items():
        try:
            follower.follow()
        except tweepy.TweepError as e:
                print(e.reason)
                pass


# begin web rendering classes here
class index(object):
    def GET(self):
        return render.index(newstring="none")

    def POST(self):
        form = web.input()
        try:
            tweetvar = "%s" % (form.tweet)
            if censor(tweetvar):
                if form.translate == "ascii":
                    tweetvar = translate(tweetvar, 'a')
                    return render.index(newstring=tweetvar)
                elif form.translate == "leet":
                    tweetvar = translate(tweetvar, 'l')
                    return render.index(newstring=tweetvar)
                else:
                    if tweet_text(tweetvar):
                        return render.confirmtweet(tweetvar=tweetvar)
            else:
                return render.confirmtweet(tweetvar="profanity")
        except:
            pass
        return render.confirmtweet(tweetvar="failure")


class confirmtweet:
    def GET(self):
        return render.confirmtweet(tweetvar="")


class features:
    def GET(self):
        return render.features()

    def POST(self):
        form = web.input(inputfile={})
        failcount = 0
        searchterms = ("%s" % (form.searchterms) if form.searchterms
                       else "#opensource")
        seconds = float(form.seconds if form.seconds else 86400)
        iterations = int(form.iterations if form.iterations else 3)
        xfollowers = int((form.xfollowers) if form.xfollowers else 3)
        if not censor(searchterms):
            return render.confirmtweet(tweetvar="profanity")
        try:
            if form.retweet:
                if retweet_follow(searchterms) is not True:
                    failcount += 1
        except:
            failcount += 1
            pass
        try:
            if form.followfollowers:
                follow_followers()
        except:
            failcount += 1
            pass
        try:
            if form.followx:
                if follow_x(searchterms, xfollowers) is False:
                        failcount += 1
        except:
            failcount += 1
            pass
        try:
            if form.autotweet:
                if 'inputfile' in form:
                    filepath = form.inputfile.filename.replace('\\', '/')
                    filename = filepath.split('/')[-1]
                    fout = open(filename, 'w')
                    fout.write(form.inputfile.file.read())
                    fout.close()
                    p = multiprocessing.Process(target=auto_tweet_file,
                                                args=(filename, seconds))
                    p.start()
        except:
            failcount += 1
            pass
        try:
            if form.autoretweet:
                p = multiprocessing.Process(target=auto_retweet,
                                            args=(searchterms, seconds,
                                                  iterations))
                p.start()
        except:
            failcount += 1
            pass
        if failcount == 5:
            return render.confirmfeature(status="failure")
        else:
            return render.confirmfeature(status="success")


class confirmfeature:
    def GET(self):
        return render.confirmfeature(status="")

if __name__ == "__main__":
    app.run()
