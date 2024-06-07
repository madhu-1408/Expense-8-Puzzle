import sys
from datetime import datetime

class Node:
    def __init__(self, data=[], parent=None, heuristic=0, depth=0, move="", cost=0):
        self.data = data
        self.parent = parent
        self.heuristic = heuristic
        self.depth = depth
        self.move = move
        self.cost = cost

n_pop, n_exp, n_gen, max_fringe_size, cost, depth_level, steps, method, dump_flag, depth_lim, fringe, vis = (0, 0, 0, 0, 0, 0, [], "a*", False, 0, [], [])

iteration = 1
now = datetime.now()
dt_string = now.strftime("%m_%d_%Y-%H_%M_%S")

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if len(sys.argv) >= 4:
        if sys.argv[3].lower() == "true":
            dump_flag = True
        elif sys.argv[3].lower() == "dls":
            method = "dls"
            depth_lim = int(input("depth limit : "))
        elif sys.argv[3].lower() in ["a*", "bfs", "dfs", "ucs", "greedy", "ids"]:
            method = sys.argv[3].lower()

    if len(sys.argv) >= 5 and sys.argv[4].lower() == "true":
        dump_flag = True
except IndexError:
    pass
except ValueError:
    pass

# Open input and output files
with open(input_file, 'r') as infile, open(output_file, 'r') as oufile:
    input_data = infile.read().split('\n')
    output_data = oufile.read().split('\n')

# Initialize matrices
input_8puzzle = []
output_8puzzle = []

# Populate matrices from input and output data
for i in range(3):
    input_8puzzle.append(list(map(int, input_data[i].split())))
    output_8puzzle.append(list(map(int, output_data[i].split())))

# Find the position of '0' in the matrix
def z_pos(matrix):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == 0:
                return i, j

# Find the position of a number in the matrix
def position(matrix, data):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == data:
                return i, j

# Calculate the Manhattan heuristic
def heuristic_2(matrix):
    h = 0
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != output_8puzzle[i][j]:
                x, y = position(output_8puzzle, matrix[i][j])
                h += (abs(x - i) + abs(y - j)) * matrix[i][j]
    return h

# Create a copy of a matrix
def dupli(matrix):
    t_mat = []
    for row in matrix:
        t_arr = list(row)  # Use list() to create a copy of the row
        t_mat.append(t_arr)
    return t_mat

def child(matrix):
    global n_gen
    x, y = z_pos(matrix.data)
    number_p_m = [[x - 1, y], [x, y - 1], [x + 1, y], [x, y + 1]]
    mat_chi = []
    
    for i in number_p_m:
        if 0 <= i[0] <= 2 and 0 <= i[1] <= 2:
            n_gen += 1
            child_n = Node()
            t_mat = dupli(matrix.data)
            t_mat[i[0]][i[1]], t_mat[x][y] = t_mat[x][y], t_mat[i[0]][i[1]]
            child_n.data = t_mat
            child_n.cost = int(t_mat[x][y]) + matrix.cost
            
            if method == "ucs":
                child_n.heuristic = matrix.heuristic + int(t_mat[x][y])
            elif method == "a*":
                child_n.heuristic = heuristic_2(t_mat) + child_n.cost
            elif method == "greedy":
                child_n.heuristic = heuristic_2(t_mat)
            else:
                child_n.heuristic = 0
                
            child_n.parent = matrix
            child_n.depth = matrix.depth + 1
            
            if i[0] < x and i[1] == y:
                child_n.move = f"{t_mat[x][y]} down"
            elif i[0] == x and i[1] < y:
                child_n.move = f"{t_mat[x][y]} right"
            elif i[0] > x and i[1] == y:
                child_n.move = f"{t_mat[x][y]} up"
            elif i[0] == x and i[1] > y:
                child_n.move = f"{t_mat[x][y]} left"
            
            mat_chi.append(child_n)
    
    return mat_chi

def btrack_data_printing(last_node):
    global cost, depth_level
    depth_level = last_node.depth
    cost = last_node.cost
    node = last_node
    while node.parent != "root":
        steps.insert(0, node.move)
        node = node.parent
    print_output()

def print_output():
    print(f"Nodes Popped: {n_pop}")
    print(f"Nodes Expanded: {n_exp}")
    print(f"Nodes Generated: {n_gen}")
    print(f"Max Fringe Size: {max_fringe_size}")
    print(f"Solution Found at depth {depth_level} with a cost of {cost}.")
    print("Steps:")
    for i in steps:
        print(f"    Move {i}")

def track_f():
    global iteration
    with open("trace-" + dt_string + ".txt", "a") as file1:
        file1.write(f"<==  iteration : {iteration} ==>\n")
        file1.write(f"Nodes Popped: {n_pop}\n")
        file1.write(f"Nodes Expanded: {n_exp}\n")
        file1.write(f"Nodes Generated: {n_gen}\n")
        file1.write("Fringe:\n")
        ll = 0
        for i in fringe:
            if method in ["a*", "greedy", "ucs"]:
                i = i["obj"]
            file1.write(f"\t\t\t{str(ll)} :: [move: {i.move}, current node cost: {i.cost}, current node: {i.data}, parent node: {i.parent.data}, heuristic: {i.heuristic}, current node depth: {i.depth}\n]")
            ll += 1
        ll = 0
        file1.write("Visited:\n")
        for j in vis:
            file1.write(f"\t\t\t{str(ll)} -> node: {j}\n")
            ll += 1
        file1.write("\n\n")
        iteration += 1

if dump_flag:
    with open("trace-" + dt_string + ".txt", "a") as file1:
        file1.write("start file :  goal file : \n")
        for i, j in zip(input_data[:3], output_data[:3]):
            file1.write(f"{i}\t\t\t{j}\n")
        file1.write(f"\nMETHOD : {method}\n")
        file1.write(f"dump_flag = {dump_flag}\n\n")
        file1.write("-----------------------------------------------------------\n")
        file1.write("Processing...... : \n\n")

def astar():
    global n_pop, n_exp, max_fringe_size, fringe
    start = Node(data=input_8puzzle, parent="root", heuristic=0, depth=0, cost=0)
    fringe.append({"h": start.heuristic, "obj": start})
    temp_max_fringe = 1
    print("a*")
    while True:
        fringe = sorted(fringe, key=lambda d: d["h"])
        current_n = fringe[0]
        n_pop += 1
        if current_n["obj"].data == output_8puzzle:
            btrack_data_printing(current_n["obj"])
            break
        if current_n["obj"].data not in vis:
            n_exp += 1
            for i in child(current_n["obj"]):
                fringe.append({"h": i.heuristic, "obj": i})
                temp_max_fringe += 1
        del fringe[0]
        temp_max_fringe -= 1
        if temp_max_fringe > max_fringe_size:
            max_fringe_size = temp_max_fringe
        vis.append(current_n["obj"].data)
        if dump_flag == True:
            track_f()

def greedy():
    global n_pop, n_exp, max_fringe_size, fringe
    start = Node(data=input_8puzzle, parent="root", heuristic=0, depth=0, cost=0)
    fringe.append({"h": start.heuristic, "obj": start})
    temp_max_fringe = 1
    print("greedy")
    while True:
        fringe.sort(key=lambda d: d["h"])
        current_n = fringe.pop(0)
        n_pop += 1
        if current_n["obj"].data == output_8puzzle:
            btrack_data_printing(current_n["obj"])
            break
        if current_n["obj"].data not in vis:
            n_exp += 1
            children = child(current_n["obj"])
            fringe.extend({"h": i.heuristic, "obj": i} for i in children)
            temp_max_fringe += len(children)
        temp_max_fringe -= 1
        max_fringe_size = max(max_fringe_size, temp_max_fringe)
        vis.append(current_n["obj"].data)
        if dump_flag:
            track_f()

def bfs():
    global n_pop, n_exp, max_fringe_size, fringe
    start = Node(data=input_8puzzle, parent="root")
    fringe.append(start)
    temp_max_fringe = 1
    while True:
        current_n = fringe.pop(0)
        n_pop += 1
        if current_n.data == output_8puzzle:
            btrack_data_printing(current_n)
            break
        if current_n.data not in vis:
            n_exp += 1
            children = child(current_n)
            fringe.extend(children)
            temp_max_fringe += len(children)
        temp_max_fringe -= 1
        max_fringe_size = max(max_fringe_size, temp_max_fringe)
        vis.append(current_n.data)
        if dump_flag:
            track_f()

def ucs():
    global n_pop, n_exp, max_fringe_size, fringe
    start = Node(data=input_8puzzle, parent="root", heuristic=0, depth=0, cost=0)
    fringe.append({"h": start.heuristic, "obj": start})
    temp_max_fringe = 1
    while True:
        fringe.sort(key=lambda d: d["h"])
        current_n = fringe.pop(0)
        n_pop += 1
        if current_n["obj"].data == output_8puzzle:
            btrack_data_printing(current_n["obj"])
            break
        if current_n["obj"].data not in vis:
            n_exp += 1
            children = child(current_n["obj"])
            fringe.extend({"h": i.heuristic, "obj": i} for i in children)
            temp_max_fringe += len(children)
        temp_max_fringe -= 1
        max_fringe_size = max(max_fringe_size, temp_max_fringe)
        vis.append(current_n["obj"].data)
        if dump_flag:
            track_f()

def dfs():
    global n_pop, n_exp, max_fringe_size, fringe
    start = Node(data=input_8puzzle, parent="root")
    fringe.append(start)
    temp_max_fringe = 1
    print("dfs is running")
    while True:
        current_n = fringe.pop()
        n_pop += 1
        if current_n.data == output_8puzzle:
            btrack_data_printing(current_n)
            break
        if current_n.data not in vis:
            n_exp += 1
            children = child(current_n)
            fringe.extend(children)
            temp_max_fringe += len(children)
        temp_max_fringe -= 1
        max_fringe_size = max(max_fringe_size, temp_max_fringe)
        vis.append(current_n.data)
        if dump_flag:
            track_f()

def dls():
    global n_pop, n_exp, max_fringe_size, fringe, depth_lim
    start = Node(data=input_8puzzle, parent="root")
    fringe.append(start)
    temp_max_fringe = 1
    flag = False
    print("dls running.....")
    while fringe:
        current_n = fringe.pop()
        n_pop += 1
        if current_n.data == output_8puzzle:
            btrack_data_printing(current_n)
            flag = True
            break
        if current_n.data not in vis and current_n.depth < depth_lim:
            n_exp += 1
            children = child(current_n)
            fringe.extend(children)
            temp_max_fringe += len(children)
        temp_max_fringe -= 1
        max_fringe_size = max(max_fringe_size, temp_max_fringe)
        vis.append(current_n.data)
        if dump_flag:
            track_f()
    if not flag:
        print(f"depth of current node more than depth limit : {depth_lim}...STOP PROGRAM, USE DIFFERENT ALGO.")

def ids():
    global n_pop, n_exp, max_fringe_size, fringe, n_gen, vis
    print("ids running.....")
    flag = False
    depth_limit = 1
    while not flag:
        n_pop = n_exp = n_gen = max_fringe_size = 0
        fringe = []
        vis = []
        start = Node(data=input_8puzzle, parent="root", depth=0)
        fringe.append(start)
        temp_max_fringe = 1
        while fringe:
            current_n = fringe.pop()
            n_pop += 1
            if current_n.data == output_8puzzle:
                btrack_data_printing(current_n)
                flag = True
                break
            if current_n.data not in vis and current_n.depth < depth_limit:
                n_exp += 1
                children = child(current_n)
                fringe.extend(children)
                temp_max_fringe += len(children)
            temp_max_fringe -= 1
            max_fringe_size = max(max_fringe_size, temp_max_fringe)
            vis.append(current_n.data)
        depth_limit += 1
        if dump_flag:
            track_f()  # Call track_f() after each iteration


if method == "a*":
    astar()
elif method == "greedy":
    greedy()
elif method == "bfs":
    bfs()
elif method == "ucs":
    ucs()
elif method == "dfs":
    dfs()
elif method == "dls":
    dls()
elif method == "ids":
    ids()
else:
    astar()