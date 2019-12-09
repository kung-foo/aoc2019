#!/usr/bin/env python3

from common import get_input

src = get_input(7)


def decode(oc):
    soc = "{:05d}".format(oc)

    cd = int(soc[3:])

    p1m = int(soc[2])
    p2m = int(soc[1])
    p3m = int(soc[0])

    # print(cd, p1m, p2m, p3m)

    return cd, p1m, p2m, p3m


def run(prog, read_input, phase, idx, done=None):
    prog = [int(v) for v in prog.split(",")]
    outp = []
    eip = 0

    read_phase = False

    last_output = None

    def fetch(addr, mode):
        if mode == 0:
            return prog[prog[addr]]
        else:
            return prog[addr]

    while True:
        op, p1m, p2m, p3m = decode(prog[eip])
        # print(idx, op, eip)
        eip += 1

        if op == 1 or op == 2:
            p1 = fetch(eip, p1m)
            p2 = fetch(eip + 1, p2m)
            p3 = fetch(eip + 2, 1)

            if op == 1:
                prog[p3] = p1 + p2
            else:
                prog[p3] = p1 * p2

            eip += 3

        elif op == 3:  # input
            p1 = fetch(eip, 1)
            # v1 = inp.pop(0)
            if not read_phase:
                v1 = phase
                read_phase = True
            else:
                # print(f"prog {idx} {read_input}")
                v1 = next(read_input)
                print(f"prog {idx} just read {v1}")
            prog[p1] = v1
            eip += 1

        elif op == 4:  # output
            v1 = fetch(eip, p1m)
            # outp.append(v1)
            last_output = v1
            print(f"prog {idx} outputs {v1}")
            yield v1
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
            print(f"prog {idx} is done")
            if done:
                done.Send(None)
            break
        else:
            # raise Exception(f"wut op: {op}")
            print(f"wut op: {op}")
            # pass
            eip += 2

    print("XXX")
    yield last_output


def amplify(src, phases):
    tail = None

    def init():
        first = True
        if first:
            print("0000000")
            yield 0
            first = False
        else:
            print("tail!")
            yield from tail

    p0 = run(src, init(), phases[0], 0)
    # return o[0]

    p1 = run(src, p0, phases[1], 1)
    # return o[0]

    p2 = run(src, p1, phases[2], 2)
    # return o[0]

    p3 = run(src, p2, phases[3], 3)
    # return o[0]

    def done():
        yield "yay!"

    p4 = run(src, p3, phases[4], 4, done)
    # return o[0]

    tail = p4

    p1.send(None)

    yield from done()

    # v = yield from p4
    # print("xxx", type(v))
    # return v


# assert run("3,0,4,0,99", [9]) == [9]

# assert run("3,9,8,9,10,9,4,9,99,-1,8", [8]) == [1]
# assert run("3,9,7,9,10,9,4,9,99,-1,8", [8]) == [0]
# assert run("3,3,1108,-1,8,3,4,3,99", [8]) == [1]
# assert run("3,3,1107,-1,8,3,4,3,99", [8]) == [0]

# list(amplify("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0]))
# print(next(x))

# assert (
#     amplify("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0]) == 43210
# )

# assert (
#     amplify(
#         "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
#         [0, 1, 2, 3, 4],
#     )
#     == 54321
# )

print(
    list(
        amplify(
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
            [9, 8, 7, 6, 5],
        )
    )
)
from itertools import permutations

# max_p = None
# max_v = 0

# for p in permutations([0, 1, 2, 3, 4]):
#     v = amplify(src, p)
#     if v > max_v:
#         max_v = v
#         max_p = p

# print(max_v, max_p)

# print(run(src, [0, 0]))
