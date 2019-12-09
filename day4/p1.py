#!/usr/bin/env python


def check(num):
    num = str(num)

    start = True
    v1 = int(num[0])
    match = False
    for c in num:
        v2 = int(c)
        if v2 < v1:
            return False
        if not start:
            if v1 == v2:
                match = True
        v1 = v2
        start = False
    return match


matches = 0
for c in range(153517, 630395):
    if check(c):
        matches += 1
print(matches)
