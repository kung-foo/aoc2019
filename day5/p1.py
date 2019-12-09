#!/usr/bin/env python3

from common import get_input

prog = get_input(5).split(",")

# prog = "3,0,4,0,99".split(",")
# prog = "1002,4,3,4,33".split(",")
inp = [1]
outp = []

prog = [int(v) for v in prog]


def decode(oc):
    soc = "{:05d}".format(oc)

    cd = int(soc[3:])

    p1m = int(soc[2])
    p2m = int(soc[1])
    p3m = int(soc[0])

    print(cd, p1m, p2m, p3m)

    return cd, p1m, p2m, p3m


def fetch(addr, mode):
    if mode == 0:
        return prog[prog[addr]]
    else:
        return prog[addr]


eip = 0
while True:
    op, p1m, p2m, p3m = decode(prog[eip])

    if op == 99:
        break

    if op == 1 or op == 2:
        p1 = fetch(eip + 1, p1m)
        p2 = fetch(eip + 2, p2m)
        p3 = fetch(eip + 3, 1)

        l = 4

        if op == 1:
            prog[p3] = p1 + p2
        else:
            prog[p3] = p1 * p2

    if op == 3:
        p1 = fetch(eip + 1, p1m)
        v1 = inp.pop(0)
        prog[p1] = v1
        l = 2

    if op == 4:
        v1 = fetch(eip + 1, p1m)
        outp.append(v1)
        l = 2

    eip += l

print(outp)
