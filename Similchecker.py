word1 = input(">> ")
word2 = input(">> ")

if len(word2) > len(word1):
    word1, word2 = word2, word1

score = 0
for i in range(len(word2)):
    for j in range(len(word1) - i):
