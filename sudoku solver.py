from itertools import combinations
from copy import deepcopy

def reduce(s, a):
    lena, returncode = 0, 0
    while len(a) != lena:
        lena = len(a)
        u = sorted(list(a.keys()))
        for idx in u:
                a[idx]=(a[idx]
                        -set(s[idx[0]])
                        -set([s[i][idx[1]] for i in range(9)])
                        -set([s[3*(idx[0]//3)+i][3*(idx[1]//3)+j]
                              for i in range(3) for j in range(3)]))
                if len(a[idx]) == 0:
                    returncode = 1
                    break
                if len(a[idx])==1:
                    s[idx[0]][idx[1]]=list(a[idx])[0]    
                    a.pop(idx)
        if returncode == 1: break
    return (s, a, returncode)
    
def decouple(s, a, u):
    for j in range(2,len(u)):
        for c in combinations(u,j):
            cu = set()
            for index in c:
                cu = cu|a[index]
            if len(cu) == j:
                for index in u-set(c):
                    a[index] = a[index]-cu
    return (s, a)

def validator(s):
    if len(s) != 9: raise TypeError 
    if set(len(line) for line in s) != {9}: raise TypeError 
    if set(i for line in s for i in line)-set(range(10)) != set(): raise TypeError 
    if len([i for line in s for i in line if i != 0]) < 17: raise TypeError
    for i in range(9):
        if len(set(s[idx[0]][idx[1]] for idx in lines[i])) != len(list(s[idx[0]][idx[1]] for idx in lines[i])): raise TypeError
        if len(set(s[idx[0]][idx[1]] for idx in columns[i])) != len(list(s[idx[0]][idx[1]] for idx in columns[i])): raise TypeError
        if len(set(s[idx[0]][idx[1]] for idx in squares[i])) != len(list(s[idx[0]][idx[1]] for idx in squares[i])): raise TypeError
    
    
            
# producing all solutions

def sudokusolver1(sudoku):

    s = deepcopy(sudoku)
    lines = [{(i,j) for j in range(9)} for i in range(9)]
    columns = [{(i,j) for i in range(9)} for j in range(9)]
    squares = [{(3*i+k,3*j+l) for k in range(3) for l in range(3)}
                for i in range(3) for j in range(3)]

    # validation
    if len(s) != 9: raise TypeError 
    if set(len(line) for line in s) != {9}: raise TypeError 
    if set(i for line in s for i in line)-set(range(10)) != set(): raise TypeError 
    if len([i for line in s for i in line if i != 0]) < 17: raise TypeError
    for i in range(9):
        if len(set(s[idx[0]][idx[1]] for idx in lines[i] if s[idx[0]][idx[1]] != 0)) != len(list(s[idx[0]][idx[1]] for idx in lines[i] if s[idx[0]][idx[1]] != 0)): raise TypeError
        if len(set(s[idx[0]][idx[1]] for idx in columns[i] if s[idx[0]][idx[1]] != 0)) != len(list(s[idx[0]][idx[1]] for idx in columns[i] if s[idx[0]][idx[1]] != 0)): raise TypeError
        if len(set(s[idx[0]][idx[1]] for idx in squares[i] if s[idx[0]][idx[1]] != 0)) != len(list(s[idx[0]][idx[1]] for idx in squares[i] if s[idx[0]][idx[1]] != 0)): raise TypeError

    # stacks
    S, C, res = [], [], []

    while True:

        # assign a set of candidates to every indeterminate
        a = {(i,j):set(range(1,10)) for j in range(9) for i in range(9) if s[i][j]==0}
        lena = 0
        while lena != sum([len(value) for value in a.values()]):
            lena = sum([len(value) for value in a.values()])

            # iteratively reduce candidate sets to admissible values and plug in if appropriate
            (s,a,returncode) = reduce(s,a)

            # check whether a solution has been found
            if returncode == 1:
                try:
                    while len(C) != 0 and len(C[-1][1]) == 0: S, C = S[:-1], C[:-1]
                    s = S[-1]
                    s[C[-1][0][0]][C[-1][0][1]] = C[-1][1][0]
                    C[-1][1] = C[-1][1][1:]
                except:
                    if len(res) != 0: return res
                    else: raise TypeError
                break
            elif len(a) == 0:
                if len(res) != 0: raise TypeError
                res = deepcopy(s)
                try:
                    while len(C) != 0 and len(C[-1][1]) == 0: S, C = S[:-1], C[:-1]
                    s = S[-1]
                    s[C[-1][0][0]][C[-1][0][1]] = C[-1][1][0]
                    C[-1][1] = C[-1][1][1:]
                except: return res
                returncode = 1
                break

            # decouple candidate sets
            for i in range(9):
                (s,a) = decouple(s,a,set(a.keys())&lines[i])
                (s,a) = decouple(s,a,set(a.keys())&columns[i])
                (s,a) = decouple(s,a,set(a.keys())&squares[i])

        # backtracking
        if returncode == 0:
            S.append(deepcopy(s))
            m = 10
            for key in a.keys():
                if len(a[key]) < m: m, k, c = len(a[key]), key, sorted(a[key])
            s[k[0]][k[1]] = c[0]
            C.append([k,c[1:]])





# uses only reduce and decouple for solving:
            
def sudokusolver2(sudoku):
    s = deepcopy(sudoku)
    if (len(s) != 9
        or set(len(line) for line in s) != {9}
        or set(i for line in s for i in line)-set(range(10)) != set()
        or len([i for line in s for i in line if i != 0]) < 17): raise TypeError 
    lines = [{(i,j) for j in range(9)} for i in range(9)]
    columns = [{(i,j) for i in range(9)} for j in range(9)]
    squares = [{(3*i+k,3*j+l) for k in range(3) for l in range(3)}
                for i in range(3) for j in range(3)]
    lena = 0
    a = {(i,j):set(range(1,10)) for j in range(9) for i in range(9) if s[i][j]==0}
    while lena != sum([len(value) for value in a.values()]):
        lena = sum([len(value) for value in a.values()])
        (s,a,returncode) = reduce(s,a)
        if returncode == 1: return "unsolvable"
        for i in range(9):
            (s,a) = decouple(s,a,set(a.keys())&lines[i])
            (s,a) = decouple(s,a,set(a.keys())&columns[i])
            (s,a) = decouple(s,a,set(a.keys())&squares[i])
    if len(a) == 0: return s
    return "No reduce and decouple solution"

            
        
# some example sudoku for trying out   


arg = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

arg = [
    [0,0,0,3,2,0,5,0,0],
    [3,7,0,0,5,0,0,0,8],
    [0,0,0,0,0,0,6,0,0],
    [0,0,0,8,0,0,0,1,0],
    [0,0,0,0,0,2,0,0,0],
    [0,3,1,0,0,0,0,4,7],
    [9,0,0,0,6,0,0,0,5],
    [1,0,2,0,0,0,9,0,0],
    [0,0,0,5,0,0,0,0,0],
    ]

arg = [
    [1,2,3,4,5,6,7,8,9],
    [4,5,6,0,0,0,0,0,0],
    [7,8,9,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]

arg = [[0, 5, 7, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 9, 0, 8, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 9, 4],
[8, 0, 0, 0, 0, 0, 0, 3, 0],
[0, 0, 2, 0, 0, 7, 0, 0, 0],
[9, 0, 0, 0, 3, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 7],
[0, 8, 0, 0, 0, 0, 0, 0, 5]]

arg = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]
