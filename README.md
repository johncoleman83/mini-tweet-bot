# <img src="https://github.com/johncoleman83/mini-tweet-bot/blob/master/static/images/anonymousface.png" width="160" height="160" /> mini tweet bot

:a python application, for twitter automation with Cloud Foundry on IBM Bluemix

### python

  * __language:__ Python 2.7.10
  * __libraries:__ tweepy, time, multiprocessing
  * __web framework:__ web.py
  * __style__: PEP 8: https://www.python.org/dev/peps/pep-0008/

### cloud:

  * __infrastructure:__ IBM Bluemix, https://www.ibm.com/cloud-computing/bluemix/
  * __platform:__ Cloud Foundry, https://www.cloudfoundry.org/
  * __Cloud Foundry command line interface (CLI):__ https://github.com/cloudfoundry/cli
  * __CF python template app:__ https://github.com/IBM-Bluemix/get-started-python

### examples:

  * __code on github:__ https://github.com/johncoleman83/mini-tweet-bot
  * __working app:__ https://mtb.mybluemix.net/
  * __blog:__ http://www.davidjohncoleman.com/2017/mini-tweet-bot/

### twitter:

  * __twitter dev tools:__ https://dev.twitter.com/
  * __tweet deck:__ https://tweetdeck.twitter.com/
  * __twitter (bot) account:__ https://twitter.com/are_no_one
  * __api limits:__ https://support.twitter.com/articles/160385
  * __best practices:__ https://dev.twitter.com/basics

## Description

This has my integrations of the tweepy python library to auto generate tweets,
retweets, and to follow users.  There is a custom integration with twitter to
allow multiple users or anyone from the public to post tweets to one specified
twitter account.  The current specified twitter account is specified above;
however, any account can be substituted such as a tourist destination twitter
account or company account.  The app is designed to run on cloudfoundry
applications with IBM Bluemix.

## Documentation

For integration with IBM Bluemix, cloudfoundry apps, see the 
[README.md](https://github.com/IBM-bluemix/get-started-python) 
from the below referenced repository.  Or read the blog post referenced above.

## File List

* `./Procfile`

  this file contains the initiation script for run the app in IBM Bluemix CF

* `./app.py`

  The main application, used to render web user interface and call all functions
  of all the features.

* `./censorship.py`

  Module with functions for censoring input text.

* `./daffodils.txt`

  Example directory to show how to input text to automate texting from a file.

* `./manifest.yml`

  Supports cloud foundry command line interface.

* `./mycredentials.py`

  Example of how to use twitter API to integrate with tweepy.  If you attempt
  to make your own twitter bot, you should rename this file `credentials.py` so
  that it is imported into `app.py` with the line: `from credentials import *`

* `./profanity.txt`

  dictionary of profaine words; contains 700+ words

* `./requirements.txt`

  contains information on the modules necessary to run this app

* `./static/`

  This directory contains all  website support files such as `.css`, `.js`, and
  fontasesome.io integrations

* `./support/`

  This directory contains old files from Cloud Foundry template, that I did not
  use.

* `./support/retweet_follow.py`, `./singletweet.py/`, `./tweet_textfile.py`

  These are example files that contain only one function for the event that
  someone wants to make a twitter bot without integration into the cloud.

* `./templates/`

  This contains all the HTML content as rendered with python

## Usage

`$ python app.py`

### Author

David John Coleman II.	Check out my website [davidjohncoleman.com](http://www.davidjohncoleman.com/)

### License

Public Domain, no copyright protection
