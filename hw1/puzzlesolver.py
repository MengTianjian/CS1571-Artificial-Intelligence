import sys
import heapq
import math
import Queue
import copy

#print sys.argv[0]
#print sys.argv[1]
class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def readfile(filename):
    f = open(filename, 'rb')
    problem = hashabledict()
    problem["type"] = f.readline().rstrip("\n")
    if problem["type"] == "monitor":
        problem["targets"] = {}
        problem["sensors"] = {}
        sensors = f.readline().split(",")
        for i in range(0, len(sensors), 4):
            if i == 0:
                sensor = sensors[i].lstrip("[(\"").rstrip("\"")
                problem["sensors"][sensor] = {}
                problem["sensors"][sensor][0] = int(sensors[i+1])
                problem["sensors"][sensor][1] = int(sensors[i+2])
                problem["sensors"][sensor][2] = int(sensors[i+3].rstrip(")"))
            elif i == len(sensors)-4:
                sensor = sensors[i].lstrip("(\"").rstrip("\"")
                problem["sensors"][sensor] = {}
                problem["sensors"][sensor][0] = int(sensors[i+1])
                problem["sensors"][sensor][1] = int(sensors[i+2])
                problem["sensors"][sensor][2] = int(sensors[i+3].rstrip(")]\n"))
            else:
                sensor = sensors[i].lstrip("(\"").rstrip("\"")
                problem["sensors"][sensor] = {}
                problem["sensors"][sensor][0] = int(sensors[i+1])
                problem["sensors"][sensor][1] = int(sensors[i+2])
                problem["sensors"][sensor][2] = int(sensors[i+3].rstrip(")"))
        targets = f.readline().split(",")
        for i in range(0, len(targets), 3):
            if i == 0:
                target = targets[i].lstrip("[(\"").rstrip("\"")
                problem["targets"][target] = {}
                problem["targets"][target][0] = int(targets[i+1])
                problem["targets"][target][1] = int(targets[i+2].rstrip(")"))
            elif i == len(targets)-3:
                target = targets[i].lstrip("(\"").rstrip("\"")
                problem["targets"][target] = {}
                problem["targets"][target][0] = int(targets[i+1])
                problem["targets"][target][1] = int(targets[i+2].rstrip(")]\n"))
            else:
                target = targets[i].lstrip("(\"").rstrip("\"")
                problem["targets"][target] = {}
                problem["targets"][target][0] = int(targets[i+1])
                problem["targets"][target][1] = int(targets[i+2].rstrip(")"))
        problem["weight"] = {}#[[0 for x in range(1+len(problem["sensors"]))] for y in range(1+len(problem["targets"]))]
        for target in problem["targets"]:
            problem["weight"][target] = {}
            for sensor in problem["sensors"]:
                problem["weight"][target][sensor] = float(problem["sensors"][sensor][2])/math.sqrt((problem["sensors"][sensor][0]-problem["targets"][target][0])**2+(problem["sensors"][sensor][1]-problem["targets"][target][1])**2)
    if problem["type"] == "aggregation":
        problem["nodes"] = {}
        problem["connections"] = {}
        nodes = f.readline().split(",")
        for i in range(0, len(nodes), 3):
            if i == 0:
                node = nodes[i].lstrip("[(\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = int(nodes[i+1])
                problem["nodes"][node][1] = int(nodes[i+2].rstrip(")"))
            elif i == len(nodes)-3:
                node = nodes[i].lstrip("(\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = int(nodes[i+1])
                problem["nodes"][node][1] = int(nodes[i+2].rstrip(")]\n"))
            else:
                node = nodes[i].lstrip("(\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = int(nodes[i+1])
                problem["nodes"][node][1] = int(nodes[i+2].rstrip(")"))
        k = 0
        for line in f:
            if line == " \n":
                break
            weight = line.rstrip("\n").split(",")
            problem["connections"][k] = {}
            problem["connections"][k][0] = weight[0].lstrip("(\"").rstrip("\"")
            problem["connections"][k][1] = weight[1].lstrip(" \"").rstrip("\"")
            problem["connections"][k][2] = int(weight[2].lstrip(" ").rstrip(")"))
            k = k+1
        #problem["weight"] = [[0 for x in range(1+len(problem["nodes"]))] for y in range(1+len(problem["nodes"]))]
        #for i in range(1, 1+len(problem["nodes"])):
        #    for j in range(1, 1+len(problem["nodes"])):
        #        problem["weight"][i][j] =
    if problem["type"] == "pancakes":
        problem["pancakes"] = {}
        pancakes = f.readline().split(",")
        for i in range(len(pancakes)):
            if i == 0:
                problem["pancakes"][i+1] = int(pancakes[i].lstrip("("))
            elif i == len(pancakes)-1:
                problem["pancakes"][i+1] = int(pancakes[i].rstrip(")\n"))
            else:
                problem["pancakes"][i+1] = int(pancakes[i])
    #print problem
    return problem

def init(problem):
    if problem["type"] == "monitor":
        node = {}
        node["state"] = ""
        node["cost"] = 0
        #node["distance"] = 0
        node["unassign"] = len(problem["targets"])
        node["targets"] = {}
        #node["targets"] = [[0 for x in range(2)] for y in range(1+len(problem["targets"]))]
        node["sensors"] = {}
        #node["sensors"] = [[0 for x in range(2)] for y in range(1+len(problem["sensors"]))]
        node["path"] = ""
        #print node
        return node
    if problem["type"] == "aggregation":
        node = {}
        node["state"] = ""
        node["delay"] = 0
        node["distance"] = 0
        node["path"] = ""
        return node
    if problem["type"] == "pancakes":
        node = {}
        node["pancakes"] = {}
        node["state"] = ""
        for i in range(len(problem["pancakes"])):
            node["pancakes"][i+1] = problem["pancakes"][i+1]
            node["state"] = node["state"] + str(node["pancakes"][i+1]) + " "
        node["path"] = node["state"]
        node["cost"] = 0
        return node

def goal_test(problem, node):
    if problem["type"] == "monitor":
        for target in problem["targets"]:
            if target not in node["targets"]:
                return False
        for sensor in problem["sensors"]:
            if sensor not in node["sensors"]:
                return False
        return True
    if problem["type"] == "aggregation":
        for key in problem["nodes"]:
            if key not in node["path"]:
                return False
        return True
    if problem["type"] == "pancakes":
        for i in range(len(problem["pancakes"])):
            if node["pancakes"][i+1] != i+1:
                return False
        return True

def get_successor_states(problem, node):
    global time
    if problem["type"] == "monitor":
        successors = Queue.Queue()#set()
        for sensor in problem["sensors"]:
            if sensor not in node["sensors"]:
                for target in problem["targets"]:
                    if sensor+"_"+target not in node["path"]:
                        new_node = copy.deepcopy(node)
                        new_node["sensors"][sensor] = -1*problem["weight"][target][sensor]
                        if target in new_node["targets"]:
                            if new_node["targets"][target] > -1*problem["weight"][target][sensor]:#< problem["weight"][t][s]:
                                new_node["targets"][target] = -1*problem["weight"][target][sensor]
                        else:
                            new_node["targets"][target] = -1*problem["weight"][target][sensor]
                        new_node["state"] = sensor+"_"+target
                        new_node["path"] = new_node["path"]+sensor+"_"+target+"\n"
                        new_node["cost"]=-1*problem["weight"][target][sensor]
                        #distance = math.sqrt((problem["sensors"][sensor][0]-problem["targets"][target][0])**2+(problem["sensors"][sensor][1]-problem["targets"][target][1])**2)
                        #new_node["distance"] = distance
                        new_node["unassign"] = len(problem["targets"]) - len(new_node["targets"])
                        time = time + 1
                        successors.put(new_node)
                return successors
    if problem["type"] == "aggregation":
        successors = Queue.Queue()
        if node["state"] == "":
            for key in problem["nodes"]:
                new_node = copy.deepcopy(node)
                new_node["state"] = key
                new_node["path"] = key
                new_node["delay"] = float('inf')
                new_node["distance"] = float('inf')
                time = time + 1
                successors.put(new_node)
        else:
            for i in range(len(problem["connections"])):
                if node["state"] == problem["connections"][i][0] and problem["connections"][i][1] not in node["path"]:
                    new_node = copy.deepcopy(node)
                    new_node["state"] = problem["connections"][i][1]
                    if new_node["delay"] == float('inf'):
                        new_node["delay"] = problem["connections"][i][2]
                    else:
                        new_node["delay"] = new_node["delay"]+problem["connections"][i][2]
                    distance = math.sqrt((problem["nodes"][new_node["state"]][0]-problem["nodes"][node["state"]][0])**2+(problem["nodes"][new_node["state"]][1]-problem["nodes"][node["state"]][1])**2)
                    #if new_node["distance"] == float('inf'):
                    new_node["distance"] = distance
                    #else:
                    #    new_node["distance"] = new_node["distance"]+distance
                    new_node["path"] = new_node["path"] + "\n" + problem["connections"][i][1]
                    time = time + 1
                    successors.put(new_node)
                elif node["state"] == problem["connections"][i][1] and problem["connections"][i][0] not in node["path"]:
                    new_node = copy.deepcopy(node)
                    new_node["state"] = problem["connections"][i][0]
                    if new_node["delay"] == float('inf'):
                        new_node["delay"] = problem["connections"][i][2]
                    else:
                        new_node["delay"] = new_node["delay"]+problem["connections"][i][2]
                    distance = math.sqrt((problem["nodes"][new_node["state"]][0]-problem["nodes"][node["state"]][0])**2+(problem["nodes"][new_node["state"]][1]-problem["nodes"][node["state"]][1])**2)
                    #if new_node["distance"] == float('inf'):
                    new_node["distance"] = distance
                    #else:
                    #    new_node["distance"] = new_node["distance"]+distance
                    new_node["path"] = new_node["path"] + "\n" + problem["connections"][i][0]
                    time = time + 1
                    successors.put(new_node)
        return successors
    if problem["type"] == "pancakes":
        successors = Queue.Queue()
        for i in range(1, 1+len(problem["pancakes"])):
            new_node = copy.deepcopy(node)
            for j in range(1, i+1):
                new_node["pancakes"][j] = -1*node["pancakes"][i+1-j]
            new_node["cost"] = new_node["cost"] + 1
            new_node["state"] = ""
            for i in range(len(new_node["pancakes"])):
                new_node["state"] = new_node["state"] + str(new_node["pancakes"][i+1]) + " "
            if new_node["state"] not in node["path"]:
                new_node["path"] = new_node["path"] + "\n" + new_node["state"]
                time = time + 1
                successors.put(new_node)
        return successors

def path_cost(problem, node):
    if problem["type"] == "monitor":
        cost = set()
        for target in problem["targets"]:
            if target in node["targets"]:
                cost.add(node["targets"][target])
        if cost == set():
            return 0
        return max(cost)#min(cost)
    if problem["type"] == "aggregation":
        return node["delay"]
    if problem["type"] == "pancakes":
        return node["cost"]

def heuristic(problem, node):
    if problem["type"] == "monitor":
        #return node["distance"]
        return node["unassign"]
    if problem["type"] == "aggregation":
        return node["distance"]
    if problem["type"] == "pancakes":
        h = 0
        for i in range(1, 1+len(node["pancakes"])):
            if node["pancakes"][i] < 0:
                h = h + 1 + abs(i+node["pancakes"][i])
            else:
                h = h + abs(i-node["pancakes"][i])
        return h

def output(problem, node):
    global maxfrontier
    global maxexplored
    global time
    print node["path"].rstrip("\n")
    print "Time: "+str(time)
    print "Space: Frontier "+str(maxfrontier)+" ,Visited "+str(maxexplored)
    if problem["type"] == "monitor":
        print "Cost "+str(-1*path_cost(problem, node))
    else:
        print "Cost "+str(path_cost(problem, node))

def bfs(problem, start):
    frontier = Queue.Queue()
    frontier.put(start)
    explored = set()
    global maxfrontier
    global maxexplored
    global time
    while not frontier.empty():
        if frontier.qsize() > maxfrontier:
            maxfrontier = frontier.qsize()
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = frontier.get()
        #print node["path"]+"\n"
        #print "\n"
        if goal_test(problem, node):
            output(problem, node)
            return True
        if node["path"] not in explored:#node["state"] not in explored:
            explored.add(node["path"])#node["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["path"] not in explored:#child["state"] not in explored:
                        frontier.put(child)
        #for child in get_successor_states(problem, node):
            #if child not in frontier:#child not in explored and child not in frontier:
                #frontier.put(child)
    print "No solution"
    return False

def unicost(problem, start):
    frontier = []
    frontierset = set()
    heapq.heappush(frontier, (path_cost(problem, start), start))
    frontierset.add(start["path"])#start["state"])
    explored = set()
    global maxfrontier
    global maxexplored
    global time
    while frontier:
        if len(frontier) > maxfrontier:
            maxfrontier = len(frontier)
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = heapq.heappop(frontier)[1]
        #print node["path"]+"\n"
        frontierset.remove(node["path"])#["state"])
        if goal_test(problem, node):
            output(problem, node)
            return True
        if node["path"] not in explored:#["state"] not in explored:
            explored.add(node["path"])#["state"])
        #    for child in get_successor_states(node):
        #        if child not in explored and child not in frontier:
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["path"] not in explored and child["path"] not in frontierset:#child["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (path_cost(problem, child), child))
                        frontierset.add(child["path"])#["state"])
                    elif child["path"] in frontierset:#child["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["path"] == child["path"] and path_cost(problem, child) < frontier[i][0]:#frontier[i][1]["state"] == child["state"] and path_cost(problem, child) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (path_cost(problem, child), child))
    print "No solution"
    return False

def greedy(problem, start):
    frontier = []
    frontierset = set()
    heapq.heappush(frontier, (heuristic(problem, start), start))
    frontierset.add(start["path"])#["state"])
    explored = set()
    global maxfrontier
    global maxexplored
    global time
    while frontier:
        if len(frontier) > maxfrontier:
            maxfrontier = len(frontier)
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = heapq.heappop(frontier)[1]
        #print node
        frontierset.remove(node["path"])#["state"])
        if goal_test(problem, node):
            output(problem, node)
            return True
        if node["path"] not in explored:#["state"] not in explored:
            explored.add(node["path"])#["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["path"] not in explored and child["path"] not in frontierset:#["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (heuristic(problem, child), child))
                        frontierset.add(child["path"])#["state"])
                    elif child["path"] in frontierset:#["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["path"] == child["path"] and heuristic(problem, child) < frontier[i][0]:#["state"] == child["state"] and heuristic(problem, child) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (heuristic(problem, child), child))
    print "No solution"
    return False

def recursivedls(problem, start, depth):
    global maxfrontier
    global maxexplored
    global time
    explored = set()
    if goal_test(problem, start):
        output(problem, start)
        return True
    elif depth == 0:
        return 0
    else:
        cutoff = False
        successors = get_successor_states(problem, start)
        if successors != None:
            while not successors.empty():
                child = successors.get()
                if child["path"] not in explored:
                    explored.add(child["path"])
            #for child in get_successor_states(start):
                result = recursivedls(problem, child, depth-1)
                if result == 0:
                    cutoff = True
                elif result != False:
                    return result
        if cutoff == True:
            return 0
        else:
            return False

def iddfs(problem, start):
    for depth in range(0,100):
        result = recursivedls(problem, start, depth)
        if result != 0:
            return result
    print "No solution"
    return False

def Astar(problem, start):
    frontier = []
    frontierset = set()
    heapq.heappush(frontier, (path_cost(problem, start)+heuristic(problem, start), start))
    frontierset.add(start["path"])
    explored = set()
    global maxfrontier
    global maxexplored
    global time
    while frontier:
        if len(frontier) > maxfrontier:
            maxfrontier = len(frontier)
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = heapq.heappop(frontier)[1]
        frontierset.remove(node["path"])#["state"])
        if goal_test(problem, node):
            output(problem, node)
            return True
        if node["path"] not in explored:#["state"] not in explored:
            explored.add(node["path"])#["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["path"] not in explored and child["path"] not in frontierset:#["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (path_cost(problem, child)+heuristic(problem, child), child))
                        frontierset.add(child["path"])#["state"])
                    elif child["path"] in frontierset:#["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["path"] == child["path"] and (path_cost(problem, child)+heuristic(problem, child)) < frontier[i][0]:#["state"] == child["state"] and heuristic(problem, child) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (path_cost(problem, child)+heuristic(problem, child), child))
    print "No solution"
    return False

time = 0
maxfrontier = 0
maxexplored = 0

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Wrong input arguments"
    filename = sys.argv[1]
    problem = readfile(filename)
    start = init(problem)
    if sys.argv[2] == 'bfs':
        bfs(problem, start)
    elif sys.argv[2] == 'unicost':
        unicost(problem, start)
    elif sys.argv[2] == 'greedy':
        greedy(problem, start)
    elif sys.argv[2] == 'iddfs':
        iddfs(problem, start)
    elif sys.argv[2] == 'Astar':
        Astar(problem, start)
