"""
censorship module
runs test on input string to see if it contains profanity
"""
from profanity import profanity


def remove_whitespace(string, sub):
    whitespace = [':', ';', '.', ',',
                  '-', '=', '*', '\t',
                  '~', '\\', '|', '\"',
                  '\'', '_', '\n']
    for i in whitespace:
        string = string.replace(i, sub)
    return string


def is_clean(inputlist):
    for word in range(0, len(inputlist)):
        for curse in profanity:
            if inputlist[word] == curse:
                return False
            temp = remove_whitespace(inputlist[word], "")
            if temp == curse:
                return False
    return True


def censor(tweetvar):
    test1 = test2 = tweetvar.lower()
    test2 = remove_whitespace(test2, " ")
    test1 = test1.split()
    test2 = test2.split()
    if is_clean(test1):
        if is_clean(test2):
            return True
    return False
