from itertools import product, permutations


# returns after a solution has been found:

def opn1(i,a,b):
    return [a + b, a * b, a - b, a / b][i]

def tf1(a,b,c,d):
    var = (a, b, c, d)
    for o in product(range(4), repeat = 3):
        for p in permutations(range(4)):
            a, b, c, d = (var[p[i]] for i in range(4))
            for t in (0,1,2,3,5):
                try:
                    x = (opn1(o[0],a,b),c,d)
                    x = (opn1(o[1],x[(0+t)%3],x[(1+t)%3]),x[(2+t)%3])
                    x = opn1(o[2],x[(0+t)%2],x[(1+t)%2])
                    if x == 24:
                        a, b, c, d = str(a), str(b), str(c), str(d)
                        o0, o1, o2 = "+*-/"[o[0]], "+*-/"[o[1]], "+*-/"[o[2]]
                        po = {(0,0):"", (0,1):"(", (1,0):"", (1,1):"", (0,2):"(", (0,3):"(", (1,2):"", (1,3):"("}
                        pc = {(0,0):"", (0,1):")", (1,0):"", (1,1):"", (0,2):")", (0,3):")", (1,2):"", (1,3):")"}
                        if t == 0:
                            return (po[(o[1]%2,o[2]%2)] + po[(o[0]%2,o[1]%2)] + a + o0 + b
                                    + pc[(o[0]%2,o[1]%2)] + o1 + c + pc[(o[1]%2,o[2]%2)] + o2 + d)
                        if t == 1:
                            return (po[(o[0]%2,o[2]%2)] + a + o0 + b + pc[(o[0]%2,o[2]%2)] + o2
                                    + po[(o[1]%2,o[2])] + c + o1 + d + pc[(o[1]%2,o[2])])
                        if t == 2:
                            return (po[(o[1]%2,o[2]%2)] + d + o1 + po[(o[0]%2,o[1])] + a + o0 + b
                                    + pc[(o[0]%2,o[1])] + pc[(o[1]%2,o[2]%2)] + o2 + c)
                        if t == 3:
                            return (d + o2 + po[(o[1]%2,o[2])] + po[(o[0]%2,o[1]%2)] + a + o0 + b
                                    + pc[(o[0]%2,o[1]%2)] + o1 + c + pc[(o[1]%2,o[2])])
                        if t == 5:
                            return (c + o2 + po[(o[1]%2,o[2])] + d + o1 + po[(o[0]%2,o[1])] + a + o0
                                    + b + pc[(o[0]%2,o[1])] + pc[(o[1]%2,o[2])])
                except: pass
    return "It\'s not possible!"


# accelerated:

def opn(i,a,b):
    if i == 0: return a + b
    if i == 1: return a * b
    if i == 2: return a - b
    if i == 3: return a / b

def tf(a,b,c,d):
    var = (a, b, c, d)
    cycles = [(0,1,2,3), (1,2,3,0), (2,3,0,1), (3,0,1,2)]
    combs = [(0,1,2,3),(0,2,1,3),(0,3,1,2),(1,2,0,3),(1,3,0,2),(2,3,0,1)]
    ordcombs = [p for p in permutations(range(4)) if p[0] < p[1]]
    perms = list(permutations(range(4)))
    trees = {
             (0,0,0):[(0,[(0,1,2,3)])],
             (0,0,1):[(0,cycles), (1,combs)],
             (0,0,2):[(0,cycles), (1,combs), (3,cycles)],
             (0,0,3):[(0,cycles), (1,combs), (3,cycles)],
             (0,1,0):[(0,ordcombs), (1,combs)],
             (0,1,1):[(0,combs)],
             (0,1,2):[(0,ordcombs), (1,combs), (3,ordcombs)],
             (0,1,3):[(0,ordcombs), (1,combs), (3,ordcombs)],
             (0,2,1):[(0,ordcombs), (1,ordcombs), (2,ordcombs)],
             (0,2,3):[(0,ordcombs), (1,ordcombs), (2,ordcombs), (3,ordcombs), (5,ordcombs)],
             (0,3,0):[(0,ordcombs), (1,ordcombs)],
             (0,3,1):[(2,ordcombs)],
             (0,3,2):[(0,ordcombs), (1,ordcombs), (2,ordcombs), (3,ordcombs), (5,ordcombs)],
             (1,0,1):[(0,ordcombs)],
             (1,0,2):[(0,ordcombs), (1,combs), (3,ordcombs)],
             (1,0,3):[(0,ordcombs), (1,ordcombs), (3,ordcombs)],
             (1,1,0):[(0,cycles), (1,combs)],
             (1,1,1):[(0,[(0,1,2,3)])],
             (1,1,2):[(0,cycles), (1,combs), (3,cycles)],
             (1,1,3):[(0,cycles), (1,perms), (3,cycles)],
             (1,2,0):[(2,ordcombs)],
             (1,2,1):[(0,ordcombs), (1,ordcombs)],
             (1,2,3):[(0,ordcombs), (1,ordcombs), (2,ordcombs), (3,ordcombs), (5,ordcombs)],
             (1,3,0):[(0,perms), (1,perms), (2,perms)],
             (1,3,2):[(0,perms), (1,perms), (2,perms), (3,perms), (5,perms)],
             (2,0,3):[(1,ordcombs)],
             (2,1,0):[(0,perms)],
             (2,1,2):[(0,perms)],
             (2,1,3):[(0,perms), (1,perms), (3,perms)],
             (2,2,1):[(1,perms)],
             (2,2,3):[(1,perms)],
             (2,3,0):[(0,perms), (1,perms), (2,perms)],
             (2,3,2):[(0,perms), (1,perms), (2,perms), (3,perms), (5,perms)],
             (3,0,1):[(0,perms)],
             (3,0,2):[(1,perms)],
             (3,0,3):[(0,perms), (3,perms)],
             (3,1,2):[(1,perms)],
             (3,2,1):[(0,perms), (2,perms)],
             (3,2,3):[(0,perms), (2,perms), (3,perms), (5,perms)],
             (3,3,0):[(1,perms)],
             (3,3,2):[(1,perms)],
             }
    for o in trees.keys():
        for tree in trees[o]:
            t = tree[0]
            for p in tree[1]:
                a, b, c, d = (var[p[i]] for i in range(4))
                try:
                    x = (opn(o[0],a,b),c,d)
                    x = (opn(o[1],x[(0+t)%3],x[(1+t)%3]),x[(2+t)%3])
                    x = opn(o[2],x[(0+t)%2],x[(1+t)%2])
                    if x == 24:
                        a, b, c, d = str(a), str(b), str(c), str(d)
                        o0, o1, o2 = "+*-/"[o[0]], "+*-/"[o[1]], "+*-/"[o[2]]
                        if t == 0: return "(("+a+o0+b+")"+o1+c+")"+o2+d
                        if t == 1: return "("+a+o0+b+")"+o2+"("+c+o1+d+")"
                        if t == 2: return "("+d+o1+"("+a+o0+b+"))"+o2+c
                        if t == 3: return d+o2+"(("+a+o0+b+")"+o1+c+")"
                        if t == 5: return c+o2+"("+d+o1+"("+a+o0+b+"))"
                except: pass
    return "It\'s not possible!"



# explanations:
#
# par (x o0 x) o1 x with po[(o0%2,o1%2)] etc
# par x o1 (x o0 x) with po[(o0%2,o1)] etc
# bracketings:
# 0: ((x0 o0 x1) o1 x2) o2 x3  (perm 012 wo switch)
# 1: (x0 o0 x1) o2 (x2 o1 x3)  (perm 120 w switch)
# 2: (x3 o1 (x0 o0 x1)) o2 x2  (perm 201 wo switch)
# 3: x3 o2 ((x0 o0 x1) o1 x2)  (perm 012 w switch)
# 5: x2 o2 (x3 o1 (x0 o0 x1))  (perm 201 w switch)
# (4 would correspond to 120 wo switch. Not needed, because covered by perms of arguments)
