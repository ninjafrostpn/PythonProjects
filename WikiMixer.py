__author__ = 'Charlie'

from random import randint as rand
import wikipedia as wiki

no = int(input("Use how many pages?\n>> "))
text = ""
names = []
for i in range(no):
    site = wiki.random()
    try:
        names.append(site)
        textin = wiki.summary(site)
        text += textin
        text += " "
    except:
        i -= 1
print("\n".join(names))
words = text.split(" ")
tuples = dict()
sanity = int(input("Input sanity level of mimicry\n>> "))

for i in range(len(words)):
    key = tuple([words[j % len(words)] for j in range(i, i + sanity)])
    tup = tuples.get(key, ())
    if len(tup) == 0:
        tuples[key] = [words[(i + sanity) % len(words)]]
        print(key)
    else:
        tuples[key].append(words[(i + sanity) % len(words)])

print(tuples)

while True:
    no = int(input("How many words?\n>> ")) - 1
    wordtup = list(list(tuples.keys())[rand(0, len(tuples))])
    gen = " ".join(list(wordtup)) + " "
    for i in range(sanity, no):
        choices = tuples[tuple(wordtup)]
        word = choices[rand(0, len(choices) - 1)]
        gen += word
        if i % 10 == 0:
            gen += "\n"
        else:
            gen += " "
        wordtup.append(word)
        wordtup.pop(0)
    print(gen)