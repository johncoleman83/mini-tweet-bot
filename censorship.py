# censorship module

def remove_whitespace(string, sub):
    whitespace = [':', ';', '.', ',',
                  '-', '=', '*', '\t',
                  '~', '\\', '|', '\"',
                  '\'', '_', '\n']
    for i in whitespace:
        string = string.replace(i, sub)
    return string


def is_clean(inputlist):
    fout = open("profanity.txt", 'r')
    profanity = fout.readlines()
    fout.close()
    for j in range(0, len(inputlist)):
        for line in profanity:
            if inputlist[j] == line[:-1]:
                return False
            temp = remove_whitespace(inputlist[j], "")
            if temp == line[:-1]:
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
