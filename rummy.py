from itertools import combinations

class Hand:

    def __init__(self, cards_lst):
        self.cards = ' '.join(cards_lst)


    def get_hand(self):
        return self.cards.split(' ')
        

    def add_card(self, newcard):
        hand = self.get_hand()
        hand.append(newcard)
        minscore = Hand(hand).get_score() + 1
        for i in range(len(hand)):
            score = Hand(hand[:i] + hand[i+1:]).get_score()
            if score < minscore:
                minscore = score
                minpos = i
        self.cards = ' '.join(hand[:minpos] + hand[minpos+1:])
        return hand[minpos]
            

    def get_score(self):

        def pieces(cards):
            if len(cards) == 0: return []
            L = [card for card in cards]
            L.sort()
            P = []
            j = 0
            while j < len(L):
                k = 0
                while j + k < len(L) and L[j+k][0] == (L[j][0] + k): k += 1
                P.append(L[j:j+k])
                j += k
            if L[0][0] == 1 and L[-1][0] == 13: P[-1].append(L[0])
            return [piece for piece in P if len(piece) >= 3]

        # translate into numbers
        c2n = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}
        v2n = {str(i): i for i in range(2, 10)}
        v2n.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1})
        hand = [(v2n[card[0]], c2n[card[1]]) for card in self.get_hand()]

        # find sets
        sets = [[cards for cards in hand if cards[0] == i] for i in range(1,14)]
        sets = [meldset for meldset in sets if len(meldset) >= 3]

        # find runs
        runs = []
        for i in range(4): runs.extend(pieces([cards for cards in hand if cards[1] == i]))

        # minimize score...
        ns, nr, minscore = len(sets), len(runs), sum(card[0] for card in hand)

        # ... by melding sets only
        minscore = min(minscore, sum(card[0] for card in hand if all(card not in meld for meld in sets)))

        # ... by melding runs only
        if nr == 2:
            intsec = set(runs[0]) & set(runs[1])
            for k in range(len(intsec)+1):
                for comb in combinations(intsec, k):
                    subset = set(comb)
                    complement = intsec - subset
                    meld = ([card for piece in pieces(set(runs[0]) - subset) for card in piece]
                            + [card for piece in pieces(set(runs[1]) - complement) for card in piece])
                    minscore = min(minscore, sum(card[0] for card in hand if card not in meld))
        if nr == 1: minscore = min(minscore, sum(card[0] for card in hand if card not in runs[0]))
            
        # ... by melding a set and a run
        if ns > 0 and nr > 0:
            for i in range(ns):
                for j in range(nr):
                    intsec = set(sets[i]) & set(runs[j])
                    for k in range(len(intsec)+1):
                        for comb in combinations(intsec, k):
                            subset = set(comb)
                            complement = intsec - subset
                            meldset = list(set(sets[i]) -subset)
                            if len(meldset) < 3: meldset = []
                            meldrun = [card for piece in pieces(set(runs[j]) - complement) for card in piece]
                            minscore = min(minscore, sum(card[0] for card in hand if card not in meldset and card not in meldrun))

        return minscore
    




cards = '2♠ 3♠ 4♠ 5♠ 3♦ 3♥ 4♥ 8♦ Q♠ K♠'
newcard = 'A♠'

cards = '5♠ 4♠ 3♣ 8♠ 5♦ 6♠ 3♦'
newcard = 'A♥'

cards1 = '5♦ 8♣ 3♥ 6♦ 4♥ 9♥ 8♦'
newcard1 = 'Q♠'

cards1 = '5♥ 3♥ A♥ 8♥ 6♣ 2♠ 5♦'
newcard1 = '4♦'

cards1 = '3♥ 2♦ 4♥ 4♠ A♠ 3♦ A♥'
newcard1 = 'K♥'

cards1 = '5♦ 6♠ 2♣ 2♥ 5♣ 8♥ 6♥'
newcard1 = 'J♠'

cards = '4♦ A♥ A♣ A♠ 5♦ 2♦ A♦'
newcard = '3♦'

cards = cards.split()

h = Hand(cards)

#print(h.cards)
#input('get_hand? ')

#print(h.get_hand())
#print(h.cards)
#input('get_score? ')

#print(h.get_score())
#print(h.cards)
#input('add_card? ')

print(h.add_card(newcard))
#print(h.cards)
#input('get_score? ')

print(h.get_score())
print(h.cards)

