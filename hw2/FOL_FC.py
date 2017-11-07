import sys

def readfile(filename):
    f = open(filename, 'rb')
    problem = {}
    problem['rule'] = {}
    i = 1
    problem['fact'] = {}
    j = 1
    problem['goal'] = {}
    for line in f:
        line = line.rstrip("\n")
        if '->' in line:
            rules = line.split("  ")
            problem['rule'][i] = {}
            k = 1
            for rule in rules:
                if "^" == rule:
                    continue
                elif "->" == rule:
                    break
                else:
                    #print rule
                    problem['rule'][i][k] = get_atom(rule)#{}
                    k += 1
                #problem['rule'][i][k]['predicate'] = rule.split("(")[0]
                #problem['rule'][i][k]['argument'] = rule.split("(")[1]
            #print rules
            problem['rule'][i]['RHS'] = get_atom(rules[2*k-2])
            i += 1
        elif 'PROVE' in line:
            #goal = line.split(" ")[1].rstrip(")\n")
            #problem['goal']['predicate'] = goal.split("(")[0]
            #problem['goal']['constant'] = goal.split("(")[1]
            goal = line.split("  ")[1]
            problem['goal'] = get_atom(goal)
        else:
            fact = line
            problem['fact'][j] = get_atom(fact)#{}
            j += 1
    print problem
    return problem

def get_atom(atom):
    atom = atom.rstrip(")").split("(")
    result = {}
    #print atom
    result['predicate'] = atom[0]
    arguments = atom[1].split(",")
    i = 1
    result['argument'] = {}
    for argument in arguments:
        result['argument'][i] = argument
        i += 1
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Wrong input arguments"
    filename = sys.argv[1]
    kb = readfile(filename)
    #fc(kb)
