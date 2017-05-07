"""
app python mini tweet bot application
takes user input and tweets to designated account
"""
import tweepy
import multiprocessing
import os
import cv2
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from time import sleep
from credentials import (consumer_key, consumer_secret, access_token,
                         access_token_secret)
from camera import take_picture
# custom imports
import censorship
from aldict import ascii_dict, leet_dict

# custom variable names from imports
remove_whitespace = censorship.remove_whitespace
censor = censorship.censor

# tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# flask integrations
app = Flask(__name__)
port = int(os.getenv('PORT', 8080))
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])


# flask support function to verify file import type
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def tweet_image(filename, tweetvar):
    """ tweets image with status """
    try:
        api.update_with_media(filename, tweetvar)
        return True
    except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False


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

# begin flask template rendering


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', newstring="none")
    if request.method == 'POST':
        tweetvar = request.form['tweet']
        if not censor(tweetvar):
            return render_template('confirmtweet.html', tweetvar="profanity")
        if request.form['translate'] == "ascii":
            tweetvar = translate(tweetvar, 'a')
        elif request.form['translate'] == "leet":
            tweetvar = translate(tweetvar, 'l')
        if request.form['action'] == 'translate':
            return render_template('index.html', newstring=tweetvar)
        else:
            if request.files['file']:
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filename)
                    if tweet_image(filename, tweetvar):
                        return render_template('confirmtweet.html',
                                               tweetvar=tweetvar)
            elif request.form['action'] == 'selfie':
                filename = take_picture()
                if tweet_image(filename, tweetvar):
                    return render_template('confirmtweet.html',
                                           tweetvar=tweetvar)
            elif tweet_text(tweetvar):
                return render_template('confirmtweet.html', tweetvar=tweetvar)
        return render_template('confirmtweet.html', tweetvar='failure')


@app.route('/confirmtweet')
def confirmtweet():
    return render_template('confirmtweet.html', tweetvar='failure')


@app.route('/features', methods=['GET', 'POST'])
def features():
    if request.method == 'GET':
        return render_template('features.html')
    if request.method == 'POST':
        failcount = 0
        searchterms = (request.form['searchterms']
                       if request.form['searchterms'] else '#opensource')
        seconds = float(request.form['seconds'] if request.form['seconds']
                        else 86400)
        iterations = int(request.form['iterations']
                         if request.form['iterations'] else 3)
        xfollowers = int(request.form['xfollowers']
                         if request.form['xfollowers'] else 3)
        if not censor(searchterms):
            return render_template('confirmtweet.html', tweetvar='profanity')
        try:
            if request.form['retweet']:
                if retweet_follow(searchterms) is not True:
                    failcount += 1
        except:
            failcount += 1
        try:
            if request.form['followfollowers']:
                follow_followers()
        except:
            failcount += 1
        try:
            if request.form['followx']:
                if follow_x(searchterms, xfollowers) is False:
                    failcount += 1
        except:
            failcount += 1
        try:
            if request.form['autotweet'] and request.files['file']:
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filename)
                    p = multiprocessing.Process(target=auto_tweet_file,
                                                args=(filename, seconds))
                    p.start()
                else:
                    failcount += 1
        except:
            failcount += 1
        try:
            if request.form['autoretweet']:
                p = multiprocessing.Process(target=auto_retweet,
                                            args=(searchterms, seconds,
                                                  iterations))
                p.start()
        except:
            failcount += 1
        if failcount >= 5:
            return render_template('confirmfeature.html', status='failure')
        else:
            return render_template('confirmfeature.html', status='success')


@app.route('/confirmfeature')
def confirmfeature():
    return render_template('confirmfeature.html', status='failure')


@app.route('/are-no-one')
def easteregg():
    return render_template('easteregg.html', status='failure')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
