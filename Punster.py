def fit(tostr, fromstr, leeway=1):
    tostr = [letter.lower() for letter in tostr]
    fromstr = [letter.lower() for letter in fromstr]
    scores = [[0 for j in range(len(fromstr))] for i in range(len(tostr))]
    highs, highscore = [], 0
    for i in range(len(tostr)):
        for j in range(len(fromstr)):
            lastchance = 0
            for k in range(min(len(tostr) - i, len(fromstr) - j)):
                if tostr[i + k] == fromstr[j + k]:
                    scores[i][j] += 1 + lastchance
                    lastchance = 0
                elif lastchance < leeway:
                    lastchance += 1
                else:
                    break
            if scores[i][j] > highscore:
                highscore = scores[i][j]
                highs = [(i, j)]
                print(i, j, scores[i][j])
            elif scores[i][j] == highscore:
                highs.append((i, j))
    returnstrs = []
    for high in highs:
        offset = 0
        returnstrlist = tostr.copy()
        for k in range(len(fromstr)):
            if k - high[1] < 0:
                returnstrlist.insert(high[0] + offset, fromstr[k])
                offset += 1
            elif k - high[1] >= highscore:
                returnstrlist.insert(high[0] + offset + highscore, fromstr[k])
                offset += 1
            else:
                returnstrlist[high[0] + offset + k] = fromstr[k]
        returnstr = ""
        for letter in returnstrlist:
            returnstr += letter
        returnstrs.append(returnstr)
    return returnstrs

while True:
    print("\n".join(fit(input("Phrase in which to fit pun\n>> "),
                        input("Word to fit in phrase for pun\n>> "))) + "\n")