#!/usr/bin/env python3

from common import get_input
from anytree import Node, RenderTree

src = get_input(6)

# src = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L"""

# src = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN"""

src = [l.strip() for l in src.split("\n")]

root = Node("COM")

nodes = {
    root.name: root,
}

for r in src:
    parent, name = r.split(")")
    node = Node(name)
    node.__aoc_parent = parent
    nodes[name] = node


for node in nodes.values():
    if node == root:
        continue
    node.parent = nodes[node.__aoc_parent]

# orbz = 0

# for node in nodes.values():
#     orbz += len(node.descendants)

# print(orbz)

you = nodes["YOU"]
san = nodes["SAN"]

syou = str(you)
ssan = str(san)

print(syou)
print(ssan)
