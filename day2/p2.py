#!/usr/bin/env python3

from common import get_input

src = get_input(2).split(",")
src = [int(v) for v in src]

# input = [1, 1, 1, 4, 99, 5, 6, 0, 99]
# print(input)

for n in range(0, 99):
    for v in range(0, 99):
        clone = list(src)

        clone[1] = n
        clone[2] = v

        eip = 0
        while True:
            oc = clone[eip]
            if oc == 99:
                break

            v1 = clone[clone[eip + 1]]
            v2 = clone[clone[eip + 2]]
            v3 = clone[eip + 3]

            if oc == 1:
                clone[v3] = v1 + v2
            if oc == 2:
                clone[v3] = v1 * v2

            eip += 4

        if clone[0] == 19690720:
            print(n, v)
            break
