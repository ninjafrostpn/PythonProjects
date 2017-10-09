__author__ = 'Charlie'
import requests
import win32api as w

def addToList(input):
    thing = input.upper()
    w.WriteProfileVal("Heap", thing, 1, "E:\Program Files\Pycharm\Projects\\Dict.moo")

word_site = "http://www.mieliestronk.com/corncob_caps.txt"
response = requests.get(word_site)

words = response.content.splitlines()
wordlist = []
wordheap = ""
for i in range(0, len(words)):
    word = str(words[i])[2: -1].upper()
    #already = w.GetProfileVal("Heap", word, "&&&", "E:\Program Files\Pycharm\Projects\\Dict.moo") == 1
    #if not already:
    #    addToList(word)
    wordlist.append(word)
    wordheap += word
    wordheap += "\n"

while True:
    conds = input("Input a comma-separated search condition\n>> ").replace(" ", "")
    fits = wordlist
    if conds[0] == "!":
        checks = conds[1: len(conds)].upper().split(",")
        for j in range(0, len(checks)):
            check = checks[j]
            if fits.count(check) > 0:
                print("Yes, %s is a word or phrase" % check)
            else:
                print("No, %s isn't a word or phrase (so far as we know)" % check)
    else:
        conds = conds.split(",")
        for i in range(0, len(conds)):
            cond = conds[i].upper()
            if cond != "":
                fits = [fits[j] for j in range(0, len(fits)) if fits[j].count(cond) > 0]
        print(fits)