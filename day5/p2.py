#!/usr/bin/env python3

from common import get_input


def decode(oc):
    soc = "{:05d}".format(oc)

    cd = int(soc[3:])

    p1m = int(soc[2])
    p2m = int(soc[1])
    p3m = int(soc[0])

    # print(cd, p1m, p2m, p3m)

    return cd, p1m, p2m, p3m


def run(prog, inp):
    prog = [int(v) for v in prog.split(",")]
    outp = []
    eip = 0

    def fetch(addr, mode):
        if mode == 0:
            return prog[prog[addr]]
        else:
            return prog[addr]

    while True:
        op, p1m, p2m, p3m = decode(prog[eip])
        eip += 1

        if op == 99:
            break

        if op == 1 or op == 2:
            p1 = fetch(eip, p1m)
            p2 = fetch(eip + 1, p2m)
            p3 = fetch(eip + 2, 1)

            if op == 1:
                prog[p3] = p1 + p2
            else:
                prog[p3] = p1 * p2

            eip += 3

        elif op == 3:
            p1 = fetch(eip, 1)
            v1 = inp.pop(0)
            prog[p1] = v1
            eip += 1

        elif op == 4:
            v1 = fetch(eip, p1m)
            outp.append(v1)
            eip += 1
        elif op == 5:
            v1 = fetch(eip, p1m)
            v2 = fetch(eip + 1, p2m)
            if v1 != 0:
                eip = v2
            else:
                eip += 2
        elif op == 6:
            v1 = fetch(eip, p1m)
            v2 = fetch(eip + 1, p2m)
            if v1 == 0:
                eip = v2
            else:
                eip += 2
        elif op == 7:
            v1 = fetch(eip, p1m)
            v2 = fetch(eip + 1, p2m)
            p3 = fetch(eip + 2, 1)
            if v1 < v2:
                prog[p3] = 1
            else:
                prog[p3] = 0
            eip += 3

        elif op == 8:
            v1 = fetch(eip, p1m)
            v2 = fetch(eip + 1, p2m)
            p3 = fetch(eip + 2, 1)
            if v1 == v2:
                prog[p3] = 1
            else:
                prog[p3] = 0
            eip += 3
        elif op == 99:
            break
        else:
            # raise Exception(f"wut op: {op}")
            print(f"wut op: {op}")
            # pass
            eip += 2

    return outp


assert run("3,0,4,0,99", [9]) == [9]

assert run("3,9,8,9,10,9,4,9,99,-1,8", [8]) == [1]
assert run("3,9,7,9,10,9,4,9,99,-1,8", [8]) == [0]
assert run("3,3,1108,-1,8,3,4,3,99", [8]) == [1]
assert run("3,3,1107,-1,8,3,4,3,99", [8]) == [0]

print(run(get_input(5), [5]))
