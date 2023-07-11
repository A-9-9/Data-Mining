"""
Data: CID, TID, Item
(1)Pruning candidate from Sn(s-extensions).
(2)Recursively doing S-step(sequence-extension step) with specific Sn.
(3)Pruning candidate from In(i-extensions).
(4)Recursively doing I-step(itemset-extension step) with specific In.
"""


"""
Questions:
(1)What does the bitmap work? Is it works for efficient counting the sequence support that 
use to judge the sequence frequency between each transaction and each node of tree?

(2)When we are pruning Sn during generation the tree, we pruning Sn by using the bitmap support 
counting the frequency   
"""


def DFS_Pruning(n, S, I):
    pass


S = [1, 2, 3, 4]
I = [1, 2, 3, 4]
DFS_Pruning(None, S, I)