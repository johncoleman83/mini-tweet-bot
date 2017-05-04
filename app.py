"""
app module
takes user input and tweets to designated account
"""
import web
import tweepy
import multiprocessing
from time import sleep
from credentials import *
import censorship
remove_whitespace = censorship.remove_whitespace
censor = censorship.censor

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
    try:
        api.update_status(tweetvar)
    except:
        return False
    return True


def retweet_follow(searchterms):
    """searches tweets with searchterms, retweets, then follows"""
    for tweet in tweepy.Cursor(api.search, q=searchterms).items(10):
        try:
            tweet.retweet()
            if not tweet.user.following:
                tweet.user.follow()
            return True
        except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False


def follow_ten(searchterms):
    """follow ten new followers based on given searchterms"""
    for x in range(10):
        for tweet in tweepy.Cursor(api.search, q=searchterms).items(50):
            try:
                if not tweet.user.following:
                    tweet.user.follow()
                    break
            except tweepy.TweepError as e:
                print(e.reason)
                pass


def auto_retweet(searchterms, seconds):
    """ searches for tweets, attempts to retweet, follows, and repeat """
    for x in range(25):
        for tweet in tweepy.Cursor(api.search, q=searchterms).items(50):
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
            if line != '\n' and censor(line):
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


class index(object):
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input()
        try:
            tweetvar = "%s" % (form.tweet)
            if censor(tweetvar):
                if tweet_text(tweetvar):
                    return render.confirmtweet(tweetvar=tweetvar)
            else:
                return render.confirmtweet(tweetvar="profanity")
        except:
            return render.confirmtweet(tweetvar="failure")
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
        try:
            if form.retweet:
                if form.searchterms:
                    searchterms = "%s" % (form.searchterms)
                    if not retweet_follow(searchterms):
                        failcount += 1
                else:
                    if not retweet_follow("#diversity"):
                        failcount += 1
        except:
            failcount += 1
            pass
        try:
            if form.followthem:
                follow_followers()
        except:
            failcount += 1
            pass
        try:
            if form.followten:
                if form.searchterms:
                    searchterms = "%s" % (form.searchterms)
                    follow_ten(searchterms)
                else:
                    follow_ten("#opensource")
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
                    try:
                        seconds = form.seconds
                        p = multiprocessing.Process(target=auto_tweet_file,
                                                    args=(filename,
                                                          float(seconds)))
                        p.start()
                    except:
                        p = multiprocessing.Process(target=auto_tweet_file,
                                                    args=(filename,
                                                          float(86400)))
                        p.start()
        except:
            failcount += 1
            pass
        try:
            if form.autoretweet:
                if form.seconds:
                    seconds = form.seconds
                else:
                    seconds = 86400
                if form.searchterms:
                    searchterms = "%s" % (form.searchterms)
                else:
                    searchterms = "#opensource #GNU"
                p = multiprocessing.Process(target=auto_retweet,
                                            args=(searchterms, float(seconds)))
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
