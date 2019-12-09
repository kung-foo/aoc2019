#!/usr/bin/env python


def check(num):
    # print(num)
    num = str(num)

    start = True
    v1 = int(num[0])
    match = False

    curr_grp = ""

    dbl = False
    # ndbl = 0

    for c in num:
        v2 = int(c)
        if v2 < v1:
            return False
        if start:
            curr_grp = c
        else:
            if v1 == v2:
                match = True
                curr_grp += c
            else:
                # print(curr_grp)
                if len(curr_grp) == 2:
                    dbl = True
                curr_grp = c
        v1 = v2
        start = False
    if len(curr_grp) == 2:
        dbl = True
    return dbl


matches = 0
for c in range(153517, 630395):
    if check(c):
        matches += 1
print(matches)

print(check(112233))
print(check(123444))
print(check(111122))
