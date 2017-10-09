__author__ = 'Charlie'
def megASCII(chars, width=20000):
    if (width != 20000) and (width != 0) and (width < 9):
        return "insufficient space"
    elif (width == 0):
        return "length of 0 is impossible"
    Hi = " /Q=Q=Q\ "  # hill
    Va = " \Q=Q=Q/ "  # valley
    Fu = "Q=Q=Q=Q=Q"  # full
    Em = "Q       Q"  # empty
    Eb = "Q/     \Q"  # empty both up
    eb = "Q\     /Q"  # empty both down
    EB = "Q<     >Q"  # empty both
    Er = "Q      \Q"  # empty right up
    er = "Q      /Q"  # empty right down
    el = "Q\      Q"  # empty left down
    BL = "         "  # blank
    l4 = "Q=Q=Q=Q\ "  # down 4-chain on left
    r4 = " /Q=Q=Q=Q"  # down 4-chain on right
    L4 = "Q=Q=Q=Q/ "  # up 4-chain on left
    R4 = " \Q=Q=Q=Q"  # up 4-chain on right
    d1 = "Q        "  # d for dots at different positions
    d3 = "    Q    "
    d4 = "      Q  "
    d5 = "        Q"
    B2 = "Q      >Q"  # B's middle
    B3 = "Q=Q=Q=Q< "
    G3 = "Q     Q=Q"  # G's middle
    M2 = "Q Q\ /Q Q"  # M's middle
    M3 = "Q  \Q/  Q"
    M4 = "Q   Q   Q"
    N2 = "Q Q\    Q"  # N's middle
    N3 = "Q  \Q\  Q"
    N4 = "Q    \Q\Q"
    J4 = "Q\   /Q  "  # J's bottom
    J5 = " \Q=Q/   "
    K2 = "Q    /Q/ "  # K's middle
    K3 = "Q=Q=Q<   "
    K4 = "Q    \Q\ "
    Q3 = "Q   Q\ /Q"  # Q's bottom
    Q4 = "Q\   \Q\ "
    Q5 = " \Q=Q/ \Q"
    S2 = "Q<       "  # S's middle
    S3 = " \Q=Q=Q\ "
    S4 = "       >Q"
    V3 = " \Q   Q/ "  # V's bottom
    V4 = "  Q\ /Q  "
    V5 = "   \Q/   "
    W4 = "Q\ /Q\ /Q"  # W's bottom
    W5 = " \Q/ \Q/ "
    X2 = " \Q\ /Q/ "  # X's middle
    X3 = "   >Q<   "
    X4 = " /Q/ \Q\ "
    Y5 = "  Q=Q=Q/ "  # last Y part
    Z2 = "     /Q/ "  # Z's middle
    Z3 = "   /Q/   "
    Z4 = " /Q/     "
    Ap = "  Q   Q  "  # For "
    r1 = "       /Q"  # single ups and downs
    l1 = "Q\       "
    R1 = "       \Q"
    L1 = "Q/       "
    l2 = "Q=Q\     "  # and 2s
    r2 = "     /Q=Q"
    L2 = "Q=Q/     "
    R2 = "     \Q=Q"
    s2 = " \Q\     "  # for the slash
    s3 = "   \Q\   "
    s4 = "     \Q\ "
    GT = "   \Q=Q\ "  # for >
    Gt = "   /Q=Q/ "
    LT = " /Q=Q/   "  # for <
    Lt = " \Q=Q\   "

    # rfrnce[A , B , C , D , E , F , G , H , I , J , K , L , M , N , O , P , Q , R , S , T , U , V , W , X , Y , Z ]
    rows = [[Hi, l4, Hi, l4, r4, Fu, r4, Em, Fu, Fu, er, d1, eb, el, Hi, l4, Hi, l4, r4, Fu, Em, Em, Em, eb, Em, Fu],
            [EB, B2, Eb, Er, d1, d1, d1, eb, d3, d4, K2, d1, M2, N2, Eb, EB, Eb, EB, S2, d3, Em, eb, M4, X2, el, Z2],
            [Fu, B3, d1, Em, Fu, Fu, G3, Fu, d3, d4, K3, d1, M3, N3, Em, L4, Q3, L4, S3, d3, Em, V3, M4, X3, R4, Z3],
            [Eb, B2, eb, er, d1, d1, Em, Eb, d3, J4, K4, d1, M4, N4, eb, d1, Q4, K4, S4, d3, eb, V4, W4, X4, S4, Z4],
            [Em, L4, Va, L4, R4, d1, Va, Em, Fu, J5, Er, Fu, Em, Er, Va, d1, Q5, Er, L4, d3, Va, V5, W5, Eb, Y5, Fu]]

    others = ["!", "?", "\"", "/", "\\", ">", "<", "=", ";", ":", ",", ".", "#", "|"]
    # refrnce[! , ? , " , / , \ , > , < , = , ; , : , , , . , # , | , ( , ) , [ , ] , + , -]
    rows2 = [[d3, Hi, Ap, r1, l1, l2, r2, BL, d3, d3, BL, BL, Ap, d3],
             [d3, Eb, Ap, Z2, s2, GT, LT, Fu, BL, BL, BL, BL, Fu, d3],
             [d3, Gt, BL, Z3, s3, S4, S2, BL, BL, BL, BL, BL, Ap, d3],
             [BL, BL, BL, Z4, s4, Gt, Lt, Fu, d3, BL, d3, BL, Fu, d3],
             [d3, d3, BL, L1, R1, L2, R2, BL, d3, d3, d3, d3, Ap, d3]]

    length = len(chars)
    lineOut = ""
    usedChars = 0
    while usedChars < length:
        usedWidth = 0
        rowsout = ["", "", "", "", ""]
        for i in range(usedChars, length):
            char = chars[i].upper()
            if (ord(char) <= ord("Z")) and (ord(char) >= ord("A")):
                if ((i == (length - 1)) and ((usedWidth + 9) > width)) or \
                        ((i != (length - 1)) and ((usedWidth + 12) > width)):
                        break
                else:
                    for j in range(0, 5):
                        rowsout[j] += rows[j][ord(char) - ord("A")]
                    usedChars += 1
                    usedWidth += 9
                    if i != (length - 1):
                        for j in range(0, 5):
                            rowsout[j] += "   "
                        usedWidth += 3
            elif char in others:
                where = others.index(char)
                if ((i == (length - 1)) and ((usedWidth + 9) > width)) or \
                        ((i != (length - 1)) and ((usedWidth + 12) > width)):
                        break
                else:
                    for j in range(0, 5):
                        rowsout[j] += rows2[j][where]
                    usedChars += 1
                    usedWidth += 9
                    if i != (length - 1):
                        for j in range(0, 5):
                            rowsout[j] += "   "
                        usedWidth += 3
            elif ord(char) == ord(" "):
                if ((usedWidth + 5) > width):
                    break
                else:
                    for j in range(0, 5):
                        rowsout[j] += BL
                    usedWidth += 5
                    usedChars += 1
            else:
                usedChars += 1
        lineOut += "\n".join(rowsout) + "\n\n"
    return lineOut

ref = len(input(">> ")) + 2
print(megASCII("the quick brown fox jumped over the lazy dog.", ref), ref, sep="\n")

while True:
    print(megASCII(input(">> "), ref))