"""
censorship module
runs test on input string to see if it contains profanity
"""
from profanity import profanity
from aldict import ascii_leet


def remove_whitespace(string, sub):
    whitespace = [':', ';', '.', ',',
                  '-', '=', '*', '\t',
                  '~', '\\', '|', '\"',
                  '\'', '_', '\n']
    for i in whitespace:
        string = string.replace(i, sub)
    return string


def leet_detect(word):
    for key in ascii_leet:
        if key in word:
            word = word.replace(key, ascii_leet[key])
    return word


def is_clean(inputlist):
    for i in range(0, len(inputlist)):
        word = inputlist[i]
        if word in profanity:
            return False
        test1 = remove_whitespace(word, "")
        if test1 in profanity:
            return False
        test2 = leet_detect(word)
        if test2 in profanity:
            return False
        test3 = leet_detect(test1)
        if test3 in profanity:
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
