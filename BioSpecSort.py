import win32api as w

q = 1
while True:
    specbits = []
    while True:
        textin = input("Input spec bits (@ to finish):\n>> ")
        if textin == "@":
            break
        else:
            specbits.append(textin.split(" "))

    for specbit in specbits:
        w.WriteProfileVal(specbit[1], str(q), " ".join(specbit),
                          "E:\Program Files\Pycharm\Projects\\Bio.spec")
        q += 1
