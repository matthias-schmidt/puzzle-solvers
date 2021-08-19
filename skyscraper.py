from itertools import combinations
from copy import deepcopy
from itertools import permutations


def ups(L):
    m, u = 0, 0
    for i in L:
        if i > m:
            u += 1
            m = i
    return u
    

def solve(clues):

    dim = len(clues)//4

    # candidates of tuples sorted by possible values of clue
    cand = {i: set() for i in range(1,dim+1)}
    for perm in permutations(range(1,dim+1)):
        cand[ups(perm)].add(perm)

    # candidates for lines and columns according to given clues
    lcand, ccand  = [], []
    for i in range(dim):
        if clues[4*dim-1-i] != 0:
            if clues[dim+i] != 0:
                lcand.append(cand[clues[4*dim-1-i]] & set(tuple(reversed(line)) for line in cand[clues[dim+i]]))
            else: lcand.append(cand[clues[4*dim-1-i]])
        else:
            if clues[dim+i] != 0:
                lcand.append(set(tuple(reversed(line)) for line in cand[clues[dim+i]]))
            else:
                lcand.append(set(permutations(range(1,dim+1))))
        if clues[i] != 0:
            if clues[3*dim-1-i] != 0:
                ccand.append(cand[clues[i]] & set(tuple(reversed(col)) for col in cand[clues[3*dim-1-i]]))
            else: ccand.append(cand[clues[i]])
        else:
            if clues[3*dim-1-i] != 0:
                ccand.append(set(tuple(reversed(col)) for col in cand[clues[3*dim-1-i]]))
            else:
                ccand.append(set(permutations(range(1,dim+1))))

    # entrywise reduction 
    lchk, cchk = -1, -1
    while sum(len(item) for item in lcand) != lchk or sum(len(item) for item in ccand) != cchk:
        lchk = sum(len(item) for item in lcand)
        cchk = sum(len(item) for item in ccand)
        for i in range(dim):
            for j in range(dim):
                intsec = set(line[j] for line in lcand[i]) & set(col[i] for col in ccand[j])
                lcand[i] = [line for line in lcand[i] if line[j] in intsec]
                ccand[j] = [col for col in ccand[j] if col[i] in intsec]

    if lchk == dim: return list(list(item[0]) for item in lcand)

    # backtracking
    lcand = [list(item) for item in lcand]
    ccand = [list(item) for item in ccand]
    sol, chk, ctr = [[] for i in range(dim)], [ccand]+[[] for i in range(dim)], [0 for i in range(dim)]
    i = 0
    while i < dim:
        while ctr[i] < len(lcand[i]):
            line = lcand[i][ctr[i]]
            ctr[i] += 1
            sol[i] = line
            chk[i+1] = [set(col for col in chk[i][j] if col[i] == line[j]) for j in range(dim)]
            if min(len(chk[i+1][j]) for j in range(dim)) > 0: break
        else: 
            i -= 2
        i += 1
    return [list(line) for line in sol]
