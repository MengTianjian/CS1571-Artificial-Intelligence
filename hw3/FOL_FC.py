import sys
import copy

def readfile(filename):
    f = open(filename, 'rb')
    problem = {}
    problem['rules'] = {}
    i = 0
    problem['facts'] = {}
    j = 0
    problem['goal'] = {}
    for line in f:
        line = line.rstrip("\n").rstrip("\r")
        if '->' in line:
            rules = line.split(" ")
            problem['rules'][i] = {}
            k = 0
            for rule in rules:
                if "^" == rule:
                    continue
                elif "->" == rule:
                    break
                else:
                    problem['rules'][i][k] = get_atom(rule)#{}
                    k += 1
            problem['rules'][i]['RHS'] = get_atom(rules[2*k])
            i += 1
        elif 'PROVE' in line:
            goal = line.split(" ")[1]
            problem['goal'] = get_atom(goal)
        else:
            fact = line
            problem['facts'][j] = get_atom(fact)#{}
            j += 1
    #print problem
    return problem

def get_atom(atom):
    atom = atom.rstrip(")").split("(")
    result = {}
    result['predicate'] = atom[0]
    arguments = atom[1].split(",")
    i = 0
    result['arguments'] = {}
    for argument in arguments:
        result['arguments'][i] = argument
        i += 1
    return result

def FOL_FC(problem, goal):
    new = 1
    while new:
        new = 0
        for i in problem['rules']:
            new += fire(problem, problem['rules'][i])
            if search(problem, goal, {}):
                return True
    return False

def fire(problem, rule):
    facts = copy.deepcopy(problem['facts'])
    assign(problem, rule, 0, {})
    return len(problem['facts'])-len(facts)

def assign(problem, rule, k, con):
    assigned = {}
    fact = copy.deepcopy(problem['facts'])
    var = False
    for i in rule[k]['arguments']:
        if rule[k]['arguments'][i][0].islower():
            if rule[k]['arguments'][i] in con:
                continue
                assigned[rule[k]['arguments'][i]] = con[rule[k]['arguments'][i]]
            else:
                var = True
                break
    if var:
        for i in fact:
            res = unify(rule[k], fact[i], con)
            if res:
                for j in res:
                    con[j] = res[j]
                if k == len(rule)-2:
                    addNewFact(problem, rule, con)
                else:
                    assign(problem, rule, k+1, con)
                for j in res:
                    del con[j]
    else:
        if search(problem, rule[k], con):
            if k == len(rule)-2:
                addNewFact(problem, rule, con)
            else:
                assign(problem, rule, k+1, con)
        '''else:
            for i in assigned:
                del con[i]'''
    '''for i in assigned:
        del con[i]'''

def search(problem, atom, con):
    fact = copy.deepcopy(atom)
    for i in fact['arguments']:
        if fact['arguments'][i][0].islower():
            fact['arguments'][i] = con[fact['arguments'][i]]
    for i in problem['facts']:
        if fact != problem['facts'][i]:
            continue
        else:
            return True
    return False

def addNewFact(problem, rule, con):
    newFact = copy.deepcopy(rule['RHS'])
    for i in newFact['arguments']:
        if newFact['arguments'][i][0].islower():
            newFact['arguments'][i] = con[newFact['arguments'][i]]
    if search(problem, newFact, {}):
        return
    problem['facts'][len(problem['facts'])] = newFact
    printfact(newFact)

def unify(atom, fact, con):
    result = {}
    if atom['predicate'] != fact['predicate']:
        return False
    elif len(atom['arguments']) != len(fact['arguments']):
        return False
    for i in atom['arguments']:
        if atom['arguments'][i][0].islower():
            if atom['arguments'][i] in con:
                if con[atom['arguments'][i]] != fact['arguments'][i]:
                    return False
                else:
                    continue
            else:
                result[atom['arguments'][i]] = fact['arguments'][i]
        else:
            if atom['arguments'][i] != fact['arguments'][i]:
                return False
    return result

inferred = ""
def printfact(atom):
    global inferred
    fact = atom['predicate']+"("
    for i in atom['arguments']:
        fact = fact+atom['arguments'][i]+","
    fact = fact.rstrip(",")+")\n"
    inferred += fact

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Wrong input arguments"
    filename = sys.argv[1]
    kb = readfile(filename)
    print FOL_FC(kb, kb['goal'])
    print inferred.rstrip("\n")
