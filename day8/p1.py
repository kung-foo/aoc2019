#!/usr/bin/env python3

from common import get_input

src = get_input(8)
# src = "0222112222120000"

dim_x = 25
dim_y = 6

# dim_x = 2
# dim_y = 2

layer_sz = dim_x * dim_y

assert len(src) % (layer_sz) == 0

layer_count = int(len(src) / (layer_sz))

layers = []
for i in range(layer_count):
    layers.append(src[i * layer_sz : (i + 1) * layer_sz])

for j, layer in enumerate(layers):
    nlayer = []
    for i in range(dim_y):
        nlayer.append(layer[i * dim_x : (i + 1) * dim_x])
    layers[j] = nlayer

# zeros = 10000
# zi = 0
# for i, layer in enumerate(layers):
#     c = str(layer).count("0")
#     if c < zeros:
#         zeros = c
#         zi = i

# print(zeros, zi)

# z6 = str(layers[6]).count("1") * str(layers[6]).count("2")
# print(z6)

output = [[" "] * dim_x for i in range(dim_y)]

for x in range(dim_x):
    for y in range(dim_y):
        stack = []
        for i, layer in enumerate(layers):
            stack.append(layer[y][x])
        print(stack)

        px = "".join(stack).lstrip("2")[0]
        if px == "1":
            output[y][x] = "*"

for row in output:
    print("".join(row))
