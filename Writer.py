__author__ = 'Charlie'

from random import randint as rand

text = ""
while True:
    textin = input("Input text for imitation (or @ when done)\n>> ")
    if textin != "@":
        text += textin
        text += " "
    else:
        break
words = text.split(" ")
links = dict()
tuples = dict()
sanity = int(input("Input sanity level of mimicry\n>> "))

for i in range(len(words)):
#    i2 = (i+1) % len(words)
#    link = links.get(words[i], [])
#    if len(link) == 0:
#        links[words[i]] = [words[i2]]
#    else:
#        links[words[i]].append(words[i2])
    key = tuple([words[j % len(words)] for j in range(i, i + sanity)])
    tup = tuples.get(key, ())
    if len(tup) == 0:
        tuples[key] = [words[(i + sanity) % len(words)]]
        print(key)
    else:
        tuples[key].append(words[(i + sanity) % len(words)])

print(links)
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