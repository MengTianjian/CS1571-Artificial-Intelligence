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
            problem["sensors"][i/4+1] = {}
            problem["sensors"][i/4+1][0] = sensors[i].lstrip(" (\"").rstrip("\"")
            problem["sensors"][i/4+1][1] = sensors[i+1]
            problem["sensors"][i/4+1][2] = sensors[i+2]
            problem["sensors"][i/4+1][3] = sensors[i+3].rstrip(")")
            if i == 0:
                problem["sensors"][i/4+1][0] = sensors[i].lstrip("[(\"").rstrip("\"")
            if i == len(sensors)-4:
                problem["sensors"][i/4+1][3] = sensors[i+3].rstrip(")]\n")
        targets = f.readline().split(",")
        for i in range(0, len(targets), 3):
            problem["targets"][i/3+1] = {}
            problem["targets"][i/3+1][0] = targets[i].lstrip(" (\"").rstrip("\"")
            problem["targets"][i/3+1][1] = targets[i+1]
            problem["targets"][i/3+1][2] = targets[i+2].rstrip(")")
            if i == 0:
                problem["targets"][i/3+1][0] = targets[i].lstrip("[(\"").rstrip("\"")
            if i == len(targets)-3:
                problem["targets"][i/3+1][2] = targets[i+2].rstrip(")]\n")
        problem["weight"] = [[0 for x in range(1+len(problem["sensors"]))] for y in range(1+len(problem["targets"]))]
        for i in range(1, 1+len(problem["targets"])):
            for j in range(1, 1+len(problem["sensors"])):
                problem["weight"][i][j] = float(problem["sensors"][j][3])/math.sqrt((int(problem["sensors"][j][1])-int(problem["targets"][i][1]))**2+(int(problem["sensors"][j][2])-int(problem["targets"][i][2]))**2)
    if problem["type"] == "aggregation":
        problem["nodes"] = {}
        problem["connections"] = {}
        nodes = f.readline().split(",")
        for i in range(0, len(nodes), 3):
            if i == 0:
                node = nodes[i].lstrip("[(\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = nodes[i+1]
                problem["nodes"][node][1] = nodes[i+2].rstrip(")")
            elif i == len(nodes)-3:
                node = nodes[i].lstrip(" (\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = nodes[i+1]
                problem["nodes"][node][1] = nodes[i+2].rstrip(")]\n")
            else:
                node = nodes[i].lstrip(" (\"").rstrip("\"")
                problem["nodes"][node] = {}
                problem["nodes"][node][0] = nodes[i+1]
                problem["nodes"][node][1] = nodes[i+2].rstrip(")")
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
    #print problem
    return problem

def init(problem):
    if problem["type"] == "monitor":
        node = {}
        node["state"] = ""
        node["cost"] = 0
        node["distance"] = 0
        node["targets"] = {}
        node["targets"] = [[0 for x in range(2)] for y in range(1+len(problem["targets"]))]
        node["sensors"] = {}
        node["sensors"] = [[0 for x in range(2)] for y in range(1+len(problem["sensors"]))]
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

def goal_test(problem, node):
    if problem["type"] == "monitor":
        for t in range(1, len(node["targets"])):
            if node["targets"][t][0] == 0:
                return False
        for s in range(1, len(node["sensors"])):
            if node["sensors"][s][0] == 0:
                return False
        return True
    if problem["type"] == "aggregation":
        for key in problem["nodes"]:
            if key not in node["path"]:
                return False
        return True

def get_successor_states(problem, node):
    if problem["type"] == "monitor":
        successors = Queue.Queue()#set()
        for s in range(1, len(node["sensors"])):
            if node["sensors"][s][0] == 0:
                for t in range(1, len(node["targets"])):
                    new_node = copy.deepcopy(node)
                    new_node["sensors"][s][0] = -1*problem["weight"][t][s]
                    new_node["sensors"][s][1] = t
                    if new_node["targets"][t][0] > -1*problem["weight"][t][s]:#< problem["weight"][t][s]:
                        new_node["targets"][t][0] = -1*problem["weight"][t][s]
                        new_node["targets"][t][1] = s
                    new_node["state"] = "S_"+str(s)+"_T_"+str(t)
                    new_node["path"] = new_node["path"]+"S_"+str(s)+"_T_"+str(t)+"\n"
                    new_node["cost"]=-1*problem["weight"][t][s]
                    distance = math.sqrt((int(problem["sensors"][s][1])-int(problem["targets"][t][1]))**2+(int(problem["sensors"][s][2])-int(problem["targets"][t][2]))**2)
                    new_node["distance"] = distance
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
                successors.put(new_node)
        else:
            for i in range(len(problem["connections"])):
                if node["state"] == problem["connections"][i][0]:
                    new_node = copy.deepcopy(node)
                    new_node["state"] = problem["connections"][i][1]
                    if new_node["delay"] == float('inf'):
                        new_node["delay"] = problem["connections"][i][2]
                    else:
                        new_node["delay"] = new_node["delay"]+problem["connections"][i][2]
                    distance = math.sqrt((int(problem["nodes"][new_node["state"]][0])-int(problem["nodes"][node["state"]][0]))**2+(int(problem["nodes"][new_node["state"]][1])-int(problem["nodes"][node["state"]][1]))**2)
                    #if new_node["distance"] == float('inf'):
                    new_node["distance"] = distance
                    #else:
                    #    new_node["distance"] = new_node["distance"]+distance
                    new_node["path"] = new_node["path"] + "\n" + problem["connections"][i][1]
                    successors.put(new_node)
                elif node["state"] == problem["connections"][i][1]:
                    new_node = copy.deepcopy(node)
                    new_node["state"] = problem["connections"][i][0]
                    if new_node["delay"] == float('inf'):
                        new_node["delay"] = problem["connections"][i][2]
                    else:
                        new_node["delay"] = new_node["delay"]+problem["connections"][i][2]
                    distance = math.sqrt((int(problem["nodes"][new_node["state"]][0])-int(problem["nodes"][node["state"]][0]))**2+(int(problem["nodes"][new_node["state"]][1])-int(problem["nodes"][node["state"]][1]))**2)
                    #if new_node["distance"] == float('inf'):
                    new_node["distance"] = distance
                    #else:
                    #    new_node["distance"] = new_node["distance"]+distance
                    new_node["path"] = new_node["path"] + "\n" + problem["connections"][i][0]
                    successors.put(new_node)
        return successors

def path_cost(problem, node):
    if problem["type"] == "monitor":
        cost = set()
        for t in range(1, len(node["targets"])-1):
            if node["targets"][t][0] != 0:
                cost.add(node["targets"][t][0])
        if cost == set():
            return 0
        return max(cost)#min(cost)
    if problem["type"] == "aggregation":
        return node["delay"]

def heuristic(problem, node):
    if problem["type"] == "monitor":
        return node["distance"]
    if problem["type"] == "aggregation":
        return node["distance"]

def bfs(problem, start):
    frontier = Queue.Queue()
    maxfrontier = 0
    maxexplored = 0
    frontier.put(start)
    explored = set()
    while not frontier.empty():
        if frontier.qsize() > maxfrontier:
            maxfrontier = frontier.qsize()
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = frontier.get()
        print node
        if goal_test(problem, node):
            print node["path"]
            print maxfrontier
            print maxexplored
            return path_cost(problem, node)
        if node["state"] not in explored:
            explored.add(node["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["state"] not in explored:
                        frontier.put(child)
        #for child in get_successor_states(problem, node):
            #if child not in frontier:#child not in explored and child not in frontier:
                #frontier.put(child)

    return False

def unicost(problem, start):
    frontier = []
    frontierset = set()
    maxfrontier = 0
    maxexplored = 0
    heapq.heappush(frontier, (path_cost(problem, start), start))
    frontierset.add(start["state"])
    explored = set()
    while frontier:
        if len(frontier) > maxfrontier:
            maxfrontier = len(frontier)
        if len(explored) > maxexplored:
            maxexplored = len(explored)
        node = heapq.heappop(frontier)[1]
        print node
        frontierset.remove(node["state"])
        if goal_test(problem, node):
            print node["path"]
            print maxfrontier
            print maxexplored
            return path_cost(problem, node)
        if node["state"] not in explored:
            explored.add(node["state"])
        #    for child in get_successor_states(node):
        #        if child not in explored and child not in frontier:
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (path_cost(problem, child), child))
                        frontierset.add(child["state"])
                    elif child["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["state"] == child["state"] and path_cost(problem, child) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (path_cost(problem, child), child))
                                #frontierset.add(child["state"])

def greedy(problem, start):
    frontier = []
    frontierset = set()
    heapq.heappush(frontier, (heuristic(problem, start), start))
    frontierset.add(start["state"])
    explored = set()
    while frontier:
        node = heapq.heappop(frontier)[1]
        print node
        frontierset.remove(node["state"])
        if goal_test(problem, node):
            print node["path"]
            return path_cost(problem, node)
        if node["state"] not in explored:
            explored.add(node["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (heuristic(problem, child), child))
                        frontierset.add(child["state"])
                    elif child["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["state"] == child["state"] and heuristic(problem, child) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (heuristic(problem, child), child))


def recursivedls(problem, start, depth):
    if goal_test(problem, start):
        print start["path"]
        return path_cost(problem, start)
    elif depth == 0:
        return 0
    else:
        cutoff = False
        successors = get_successor_states(problem, start)
        #print successors
        while not successors.empty():
            child = successors.get()
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

def Astar(problem, start):
    frontier = []
    frontierset = set()
    heapq.heappush(frontier, (path_cost(problem, start)+heuristic(problem, start), start))
    frontierset.add(start["state"])
    explored = set()
    while frontier:
        node = heapq.heappop(frontier)[1]
        frontierset.remove(node["state"])
        if goal_test(problem, node):
            print node["path"]
            return path_cost(problem, node)
        if node["state"] not in explored:
            explored.add(node["state"])
            successors = get_successor_states(problem, node)
            if successors != None:
                while not successors.empty():
                    child = successors.get()
                    if child["state"] not in explored and child["state"] not in frontierset:
                        heapq.heappush(frontier, (path_cost(problem, start)+heuristic(problem, child), child))
                        frontierset.add(child["state"])
                    elif child["state"] in frontierset:
                        for i in range(len(frontier)):
                            if frontier[i][1]["state"] == child["state"] and (path_cost(problem, start)+heuristic(problem, child)) < frontier[i][0]:
                                frontier.remove(frontier[i])
                                heapq.heapify(frontier)
                                heapq.heappush(frontier, (path_cost(problem, start)+heuristic(problem, child), child))


def main():
    print sys.argv[0]
    print sys.argv[1]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Wrong input arguments"
    filename = sys.argv[1]
    problem = readfile(filename)
    start = init(problem)
    if sys.argv[2] == 'bfs':
        print bfs(problem, start)
    elif sys.argv[2] == 'unicost':
        print unicost(problem, start)
    elif sys.argv[2] == 'greedy':
        print greedy(problem, start)
    elif sys.argv[2] == 'iddfs':
        print iddfs(problem, start)
    elif sys.argv[2] == 'Astar':
        print Astar(problem, start)
