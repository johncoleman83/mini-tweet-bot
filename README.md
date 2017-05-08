# <img src="https://github.com/johncoleman83/mini-tweet-bot/blob/master/static/images/anonymousface.png" width="160" height="160" /> mini tweet bot

:a python application, for twitter automation with Cloud Foundry on IBM Bluemix

### python

  * __language:__ Python 3.6.1
  * __libraries:__ tweepy, time, multiprocessing, opencv-python, numpy, workzeug
  * __web framework:__ flask
  * __style__: PEP 8: https://www.python.org/dev/peps/pep-0008/
  	* Note: for python-2.7.10, download the .zip file from the Release v0.0.4 -
	this older release uses web.py:
	* https://github.com/johncoleman83/mini-tweet-bot/releases/tag/v0.0.4

### cloud:

  * __infrastructure:__ IBM Bluemix, https://www.ibm.com/cloud-computing/bluemix/
  * __platform:__ Cloud Foundry, https://www.cloudfoundry.org/
  * __Cloud Foundry command line interface (CLI):__ https://github.com/cloudfoundry/cli
  * __CF python template app:__ https://github.com/IBM-Bluemix/get-started-python

### examples:

  * __working app:__ https://mtb.mybluemix.net/
  * __blog:__ http://www.davidjohncoleman.com/2017/mini-tweet-bot/

### twitter:

  * __twitter dev tools:__ https://dev.twitter.com/
  * __tweet deck:__ https://tweetdeck.twitter.com/
  * __twitter (bot) account:__ https://twitter.com/are_no_one
  * __api limits:__ https://support.twitter.com/articles/160385
  * __best practices:__ https://dev.twitter.com/basics

## description

This has my integrations of the tweepy python library to auto generate tweets,
retweets, and to follow users.  There is a custom integration with twitter to
allow multiple users or anyone from the public to post tweets to one specified
twitter account.  The current specified twitter account is specified above;
however, any account can be substituted such as a tourist destination twitter
account or company account.  The app is designed to run on cloudfoundry
applications with IBM Bluemix.

## documentation

For integration with IBM Bluemix, cloudfoundry apps, see the 
[README.md](https://github.com/IBM-bluemix/get-started-python) 
from the below referenced repository.  Or read the blog post referenced above.

## file List

### cloud foundry

* `./Procfile`: this file contains the initiation script for run the app
in IBM Bluemix CF
* `./manifest.yml`: Supports cloud foundry command line interface.
* `./runtime.txt`: informs cloudfoundry of what version of python to run
* `./requirements.txt`: contains the required python libraries to be installed
  during the cloudfoundry building process

### python app files

* `./app.py`

  The main application, used to render web user interface and call all functions
  of all the features.

* `./censorship.py`

  Module with functions for censoring input text.

* `./mycredentials.py`

  Example of how to use twitter API to integrate with tweepy.  If you attempt
  to make your own twitter bot, you should rename this file `credentials.py` so
  that it is imported into `app.py` with the line: `from credentials import *`

### Dictionaries:

  * `./profanity.py`, `./suppprt/profanity.txt`, `aldict.py`

  `profanity.py`: set of profaine words; contains 700+ words.  the `.py`
  file contains a set and is imported into the `censorship.py` module, the
  `.txt` file is used simply for testing and to more easily share the
  list.  `aldict.py` contains the ascii-art and L337 translation
  dictionaries

### `./static/`

  This directory contains all  website support files such as `.css`, `.js`, and
  fontasesome.io integrations

### `./support/`

  This directory contains old files from Cloud Foundry template, that I did not
  use, and some other support files explained below.

* `./support/daffodils.txt`

  Example file to show how to input text to automate texting from a file. Each
  line from the file is tweeted every N seconds.

* `./support/retweet_follow.py`, `./singletweet.py/`, `./tweet_textfile.py`

  These are example files that contain only one function for the event that
  someone wants to make a twitter bot without integration into the cloud.

### `./templates/`

  This contains all the HTML content as rendered with python.  I used one file
  as a base layout which contains the same head, header, sidebar, and footer.
  The main content in the article section changes per GET and POST call.

### `./uploads/`

  directory to store uploads from user input

## usage

* from local machine:

  ```
  $ python3 app.py
  ```

* with cloudfoundry CLI:

  ```
  $ cf login -a api.[my-cloudfoundry].com
  $ cd [my-app-directory]
  $ cf push -b https://github.com/heroku/heroku-buildpack-python.git
  ```
  Note: use latest heroku python buildpack for most updated python & pip
  versions

## build your own bot

   * fork or clone the github repository.
   * get your own twitter app from twitter dev tools linked above.
   * change the `mycredentials.py` file name to `credentials.py`
   * change the strings from the credentials file to contain your personal
   	 twitter information.
   * change the twitter feed link in the <aside> HTML tag to instead link to
   	 your twitter feed.
   * change the link of the twitter handle in the nav HTML tag to link instead
   	 to your linked twitter account.
   * change the icon/ logos to your preference
   * find the cloud to host the app.  Mini tweet bot is already setup with
   	 Cloud Foundry for IBM Bluemix, but other cloud services will work as well.

__NOTE:__ The mini tweet bot functions most successfully when hosted on a
cloud.  However, if you would like to run the app on your own machine, you can
run it, and it will be loaded on a local host port IP address such as:
http://0.0.0.0:8080/.  If you do not want the user interface, you should then
use only the tweet functions, and run them on an as needed basis.  Here is an
example of how to run a single function from the `singletweet.py` file in the
`./support` directory:

```
$ cat singletweet.py
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
$ python singletweet.py
```

### Author

David John Coleman II.	Check out my website [davidjohncoleman.com](http://www.davidjohncoleman.com/)

### License

Public Domain, no copyright protection
