__author__ = 'Charlie'

from random import randint as rand
import wikipedia as wiki

def stripout(passage, takeout, putin=" "):
    try:
        for c in takeout:
            passage = putin.join(passage.split(c))
        return passage
    except:
        return putin.join(passage.split(takeout))
    
ambiguous = False
names = []
while not ambiguous:
    subject = input("What to search for?\n>> ")
    # names = wiki.search(subject, 10)
    print("Finding Disambiguation page:")
    try:
        print("-" + subject + "(Disambiguation)")
        wiki.page(subject + "(Disambiguation)")
    except wiki.DisambiguationError as e:
        names = e.options
        print("--Selected")
        break
    except:
        pass
    print("--Discounted")
    for searchresult in wiki.search(subject, 10):
        print("-" + searchresult)
        try:
            wiki.page(searchresult)
            print("--Discounted")
        except wiki.DisambiguationError as e:
            ambiguous = True
            names = e.options
            print("--Selected")
            break
    if not ambiguous:
        print("-No Disambiguation Page Found")

print("Obtaining summaries:")
summaries = []
for name in names:
    print("-" + name)
    try:
        summaries.append(wiki.page(name, auto_suggest=False).summary)
        print("--Added")
    except wiki.DisambiguationError:
        print("--Discounted")
    except Exception as e:
        print("--Error:")
        print("---" + str(e))
print(summaries)
print("Processing Text")
words = " ".join(summaries)
print(words)
words = stripout(words, ["\n", "  ", "\t"]).split(" ")

tuples = dict()
while True:
    try:
        sanity = int(input("Input sanity level of mimicry\n>> "))
        break
    except:
        print("Invalid numerical input")

print("Finding connections")
for i in range(len(words)):
    key = tuple([words[j % len(words)] for j in range(i, i + sanity)])
    tup = tuples.get(key, ())
    if len(tup) == 0:
        tuples[key] = [words[(i + sanity) % len(words)]]
        print(key)
    else:
        tuples[key].append(words[(i + sanity) % len(words)])

print(tuples)

starts = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

while True:
    while True:
        try:
            no = int(input("Minimum number of words?\n>> "))
            break
        except:
            print("Invalid numerical input")
    while True:
        wordtup = list(list(tuples.keys())[rand(0, len(tuples))])
        try:
            if wordtup[0][0] in starts:
                break
        except:
            pass
    gen = " ".join(list(wordtup)) + " "
    count = sanity
    while count < no or gen[-2] != ".":
        choices = tuples[tuple(wordtup)]
        word = choices[rand(0, len(choices) - 1)]
        gen += word
        if count % 10 == 0:
            gen += "\n"
        else:
            gen += " "
        wordtup.append(word)
        wordtup.pop(0)
        count += 1
    print(gen)