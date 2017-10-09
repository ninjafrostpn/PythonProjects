trans = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()

while True:
    words = input("Input words\n>>> ").split()

    code = []
    for word in words:
        for letter in word:
            code.append(trans[ord(letter) - ord('a')])
        code.append("\n")
    code = "  ".join(code)
    snek = ""
    for i in code:
        if i == ".":
            snek += "Sn "
        elif i == "-":
            snek += "ek "
        else:
            snek += i
    print(snek)
