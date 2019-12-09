from common import get_input


def decode(i):
    return i[0], int(i[1:])


src = get_input(3).split("\n")

w1 = src[0].split(",")
w2 = src[1].split(",")

# w1 = "R8,U5,L5,D3".split(",")
# # w1 = "L1,D1,R2,U1,R7,U5,L5,D3".split(",")
# w2 = "U7,R6,D4,L4".split(",")

# # w1 = "R8,U5,L5,D3".split(",")
# # w2 = "U0".split(",")

# w1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
# w2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")

# w1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
# w2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")

sx = 0
sy = 0

w_max_x = 0
w_min_x = 0
w_max_y = 0
w_min_y = 0

w_max_x = 0
w_min_x = 0
w_max_y = 0
w_min_y = 0

for op in w1:
    d, v = decode(op)

    if d == "R":
        sx += v
    if d == "L":
        sx -= v
    if d == "U":
        sy += v
    if d == "D":
        sy -= v

    if sx > w_max_x:
        w_max_x = sx

    if sx < w_min_x:
        w_min_x = sx

    if sy > w_max_y:
        w_max_y = sy

    if sy < w_min_y:
        w_min_y = sy

sx = 0
sy = 0

for op in w2:
    d, v = decode(op)

    if d == "R":
        sx += v
    if d == "L":
        sx -= v
    if d == "U":
        sy += v
    if d == "D":
        sy -= v

    if sx > w_max_x:
        w_max_x = sx

    if sx < w_min_x:
        w_min_x = sx

    if sy > w_max_y:
        w_max_y = sy

    if sy < w_min_y:
        w_min_y = sy

# print(w_min_x, w_max_x)
# print(w_min_y, w_max_y)

offset_x = -w_min_x
offset_y = -w_min_y


x_dim = w_max_x - w_min_x + 1
y_dim = w_max_y - w_min_y + 1
# print(x_dim, y_dim)

board = [["."] * x_dim for i in range(y_dim)]
steps = [[0] * x_dim for i in range(y_dim)]

intersections = []

update_steps = True


def set_x(x, y, l, marker, dist):
    step = 1
    if l < 0:
        step = -1
        x -= 1
    else:
        x += 1
        pass

    s = 1
    for i in range(x, x + l, step):
        # print(x, y, i, len(board[y]))
        if board[y][i] != "." and board[y][i] != marker:
            intersections.append((y, i, steps[y][i] + dist + s))
            board[y][i] = "X"
        else:
            board[y][i] = marker
        steps[y][i] = dist + s
        s += 1
    # board[y][i] = "+"


def set_y(x, y, l, marker, dist):
    step = 1
    if l < 0:
        step = -1
        y -= 1
    else:
        y += 1
        pass

    s = 1
    for i in range(y, y + l, step):
        if board[i][x] != "." and board[i][x] != marker:
            # intersections.append((i, x))
            intersections.append((i, x, steps[i][x] + dist + s))
            board[i][x] = "X"
        else:
            board[i][x] = marker
        steps[i][x] = dist + s
        s += 1
    # board[i][x] = "+"


sx = offset_x
sy = offset_y

dist = 0
for op in w1:
    # print(op)
    d, v = decode(op)

    if d == "R":
        set_x(sx, sy, v, "a", dist)
        sx += v
    if d == "L":
        set_x(sx, sy, -v, "a", dist)
        sx -= v
    if d == "U":
        set_y(sx, sy, v, "a", dist)
        sy += v
    if d == "D":
        set_y(sx, sy, -v, "a", dist)
        sy -= v

    dist += v

sx = offset_x
sy = offset_y

update_steps = False

dist = 0
for op in w2:
    # print(op)
    d, v = decode(op)

    if d == "R":
        set_x(sx, sy, v, "b", dist)
        sx += v
    if d == "L":
        set_x(sx, sy, -v, "b", dist)
        sx -= v
    if d == "U":
        set_y(sx, sy, v, "b", dist)
        sy += v
    if d == "D":
        set_y(sx, sy, -v, "b", dist)
        sy -= v

    dist += v

board[offset_y][offset_x] = "o"

# board.reverse()
# for row in board:
#     for col in row:
#         print(col, end="")
#     print()

print("offset", offset_x, offset_y)


closest = 1000000
dists = []

for i in intersections:
    # print(i)
    # print(i[0] - offset_y, i[1] - offset_x)
    md = abs(i[0] - offset_y) + abs(i[1] - offset_x)
    # print(md)
    # print()
    dists.append((md, i[2]))
    # print()
    if md == 0:
        continue

    if md < closest:
        closest = md

# dists.sort()
dists.sort(key=lambda x: x[1])
print(dists)

