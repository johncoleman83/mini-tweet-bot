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

### `./static/uploads/`

  directory to store uploads from user input
  