__author__ = 'Charlie'

import requests, wikipedia

word_site = "https://en.wikipedia.org/wiki/Special:Random"
response = requests.get(word_site)

words = response.content.splitlines()

for w in range(len(words)):
    words[w] = str(words[w])

print("\n".join(words))

#import colorama as c
#c.init()
#print("\033[2J")

#imp = ""
#pmi = 0
#while True:
#    imp = input(">> ")
#    if imp != "w":
#        pmi += 1
#    else:
#        break
#print(pmi, imp, sep=" ")

# print([chr(i) for i in range(ord("A"), ord("Z") + 1)])
# print(input(">> ").replace("'", ""))