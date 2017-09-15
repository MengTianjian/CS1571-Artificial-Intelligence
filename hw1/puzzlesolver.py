import sys

#print sys.argv[0]
#print sys.argv[1]

def bfs():

def unicost():

def greedy():

def iddfs():

def Astar():



def main():
    print sys.argv[0]
    print sys.argv[1]

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Wrong input arguments"
    elif sys.argv[2] == 'bfs':
        bfs(sys.argv[1])
    elif sys.argv[2] == 'unicost':
        unicost(sys.argv[1])
    elif sys.argv[2] == 'greedy':
        greedy(sys.argv[1])
    elif sys.argv[2] == 'iddfs':
        iddfs(sys.argv[1])
    elif sys.argv[2] == 'Astar':
        Astar(sys.argv[1])
