#!/usr/bin/env python3

from common import get_input

input = get_input(2).split(",")
input = [int(v) for v in input]

# input = [1, 1, 1, 4, 99, 5, 6, 0, 99]
# print(input)

input[1] = 12
input[2] = 2

eip = 0
while True:
    oc = input[eip]
    if oc == 99:
        break

    v1 = input[input[eip + 1]]
    v2 = input[input[eip + 2]]
    v3 = input[eip + 3]

    if oc == 1:
        input[v3] = v1 + v2
    if oc == 2:
        input[v3] = v1 * v2

    eip += 4

print(input)
