def bogglecheck(board,word):
    if len(word) == 0: return False
    pos = {letter:[] for letter in set(word)}
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] in word: pos[board[i][j]].append((i,j))
    for value in pos.values():
        if len(value) == 0: return False
    cand = [[pair] for pair in pos[word[0]]]
    k = 1
    while k < len(word):
        cand = [path+[pair] for path in cand for pair in pos[word[k]]
                if path[-1][0]-pair[0]+1 in range(3)
                and path[-1][1]-pair[1]+1 in range(3)
                and pair not in path]
        if len(cand) == 0: return False
        k += 1
    return True
