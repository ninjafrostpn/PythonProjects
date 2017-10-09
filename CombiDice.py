def simplifract(num, den):
    g = min(num, den)
    while g > 1:
        if num % g == 0 and den % g == 0:
            num /= g
            den /= g
            g = min(num, den)
        g -= 1
    return "%d/%d" %(num, den)

while True:
    dices = []  # haha... pedants, revolt!
    while True:
        dicin = input("Input dice code\n>> ")
        try:
            if dicin == "help":
                # for if you need help understanding
                pass
            elif dicin == "@":
                # to symbolise no mo dice
                break
            else:
                # remove the spaces and lowercasify
                dicin = "".join(dicin.lower().split(" "))
                dicin = dicin.split(",")
                if dicin == [""]:
                    print("At least write SOMETHING...")
                else:
                    faces = []
                    for f in dicin:
                        # to be clear, dicin is one die input
                        # f is one of the faces or face sets given for that die
                        if "t" in f:
                            # xty means all integers between x and y inclusive
                            # hence 1t6 is equivalent to d6
                            ns = f.split("t")
                            for n in range(int(ns[0]), int(ns[1])+1):
                                faces.append(n)
                        elif "d" == f[0]:
                            # prefixing a number n with d means 1-n
                            for n in range(1, int(f[1:])+1):
                                faces.append(n)
                        else:
                            # does support just integers... no floats yet
                            faces.append(int(f))
                    dices.append(faces)
                    no = len(faces)
                    if no == 1:
                        print("So... a one sided die with face %d" %(faces[0]))
                    else:
                        print("Okay, so faces on that die are %s and %d" %(str(faces[:no-1])[1:-1], faces[no-1]))
        except:
            print("That... does not look right.\nRun that by me again?")
    print("Got your dice, calculating possibilities...")
    itr8 = [0 for k in range(len(dices))]
    coms = dict()
    done = False
    while not done:
        tot = sum([dices[n][itr8[n]] for n in range(len(dices))])
        tally = coms.get(tot, 0)
        coms[tot] = tally + 1
        i = 0
        while True:
            if i == len(dices):
                done = True
                break
            itr8[i] += 1
            if itr8[i] % len(dices[i]) == 0:
                itr8[i] = 0
                i += 1
            else:
                break
    print("Done calculating possibilities, printing in order of decreasing likelihood (sum >> probability[2DP])...")
    val = list(coms.keys())
    freq = list(coms.values())
    freqtot = sum(freq)
    for i in range(len(coms)):
        j = freq.index(max(freq))
        print("%d >> %d/%d = %s = %.4f" %(val[j], freq[j], freqtot, simplifract(freq[j],freqtot), freq[j]/freqtot))
        val.pop(j)
        freq.pop(j)
    print("Here we go again")