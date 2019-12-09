from common import get_input


def decode(i):
    return i[0], int(i[1:])


src = get_input(3).split("\n")

w1 = src[0].split(",")
w2 = src[1].split(",")

# w1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
# w2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")

seth = {"R": "seth 90", "U": "seth 0", "D": "seth 180", "L": "seth 270"}

cmds = ["home"]

cmds.append('setpencolor "red')
for op in w1:
    d, v = decode(op)

    cmds.append(seth[d])
    cmds.append(f"fd {v}")

cmds.append("pu")
cmds.append("home")
cmds.append("pd")
cmds.append('setpencolor "blue')
for op in w2:
    d, v = decode(op)

    cmds.append(seth[d])
    cmds.append(f"fd {v}")

cmds.append("hideturtle")

with open("turtle.prog", "w") as f:
    f.write("\n".join(cmds))
