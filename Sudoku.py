__author__ = 'Charlie'

whole = [["123456789" for i in range(9)] for j in range(9)]

for i in range(9):
    for j in range(9):
        noin = input("Enter number at position %d,%d\n>> " % (i, j))
        if len(noin) > 0:
            whole[i][j] = noin
            for k in range(9):
                if k != i:
                    whole[k][j].replace(noin, "")
                if k != j:
                    whole[i][k].replace(noin, "")
            sx = i - (i%3)
            sy = j - (j%3)
            for p in range(sx, sx+3):
                for q in range(sy, sy+3):
                    if not (i == p and j == q):
                        whole[p][q].replace(noin, "")

while True:
    for i in range(9):
        for j in range(9):
            n = sol[i][j]
            if len(n) == 1:
                for k in range(9):
                    if k != i:
                        whole[int(n)][j].replace(n, "")
                    if k != j:
                        whole[i][int(n)] = sol[i][int(n)].replace(n, "")
            else:
                pass