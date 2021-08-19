def bfv(M):
    n = 10
    req = [4, 3, 2, 1]
    count = [0, 0, 0, 0]
    for i in range(n):
        for j in range(n):
            if M[i][j] == 1:
                if i < n-1:
                    if j > 0 and M[i+1][j-1] == 1: return False
                    if j < n-1 and M[i+1][j+1] == 1: return False
                if (i == 0 or M[i-1][j] == 0) and (j == 0 or M[i][j-1] == 0):
                    lh, lv = 1, 1
                    while j+lh < n and M[i][j+lh] == 1: lh += 1
                    while i+lv < n and M[i+lv][j] == 1: lv += 1
                    if lh > 1 and lv > 1: return False
                    if max(lh,lv)-1 >= len(count): return False
                    count[max(lh,lv)-1] += 1
    return count == req
                
                    
# examples of puzzles for trying out

M = [[1,1,1,0,0,1],[0,0,0,0,0,1],
     [1,1,1,0,0,1],[0,0,0,0,0,1],
     [1,1,0,0,0,0],[0,0,1,0,0,0]]
     
M = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
     [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
     [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
