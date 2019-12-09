#!/usr/bin/env python3
from common import get_input
from math import floor

# take its mass, divide by three, round down, and subtract 2.


def fuel_req(mass):
    if mass == 0:
        return 0
    return floor(mass / 3) - 2


f = 0
for line in get_input(1).strip().split("\n"):
    f += fuel_req(int(line))

print(f)
