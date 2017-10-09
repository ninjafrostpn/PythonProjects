from random import randint as rand

__author__ = 'Charlie'

while True:
    target = input("Input target phrase\n>> ").upper()
    start = "#"*len(target)
    notdone = [i for i in range(0, len(start))]
    i = 0

    while start != target:
        r1 = rand(ord('A'), ord('Z') + 2)
        if r1 > ord('Z'):
            rep = " "
        else:
            rep = chr(r1)
        r2 = rand(0, len(notdone) - 1)
        pos = notdone[r2]
        i += 1
        #print("%d: Substitute %d (%s) with %s" %(i, r2, start[r2], rep))
        if pos == len(start) - 1:
            start = start[:pos] + rep
        else:
            start = start[:pos] + rep + start[pos+1:]
        if start[pos] == target[pos]:
            notdone.remove(pos)
        print(start, i)