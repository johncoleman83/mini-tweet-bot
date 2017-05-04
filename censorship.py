# censorship module

def remove_whitespace(string, sub):
    whitespace = [':', ';', '.', ',',
                  '-', '=', '*', '\t',
                  '~', '\\', '|', '\"',
                  '\'', '_', '\n']
    for i in whitespace:
        string = string.replace(i, sub)
    return string


def censor(tweetvar):
    test1 = test2 = tweetvar.lower()
    test2 = remove_whitespace(test2, " ")
    test1 = test1.split()
    test2 = test2.split()
    fout = open("profanity.txt", 'r')
    profanity = fout.readlines()
    fout.close()
    for j in range(0, len(test1)):
        for line in profanity:
            if test1[j] == line[:-1]:
                return False
            temp = remove_whitespace(test1[j], "")
            if temp == line[:-1]:
                return False
    for j in range(0, len(test2)):
        for line in profanity:
            if test2[j] == line[:-1]:
                return False
    return True
