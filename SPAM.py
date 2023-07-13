"""
Data: CID, TID, Item
(1) Pruning candidate from Sn(s-extensions).
(2) Recursively doing S-step(sequence-extension step) with specific Sn.
(3) Pruning candidate from In(i-extensions).
(4) Recursively doing I-step(itemset-extension step) with specific In.
"""
from input_ import calculate_support

"""
Questions:
(1) What does the bitmap work? Is it works for efficient counting the sequence support that 
    use to judge the sequence frequency between each transaction and each node of tree?
(2) When we are pruning Sn during generation the tree, we pruning Sn by using the bitmap support 
    counting the frequency   
"""

"""
Parameter definition:
minSup: Support threshold  
"""
support = 1
bitmaps = [
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]
S = [0, 1, 2, 3]
I = [0, 1, 2, 3]

# Definition for Lexicographic tree node.
class TreeNode:
    def __init__(self, val, bit_map, sub_nodes):
        self.val = val
        self.bit_map = bit_map
        self.sub_nodes = sub_nodes


def I_step(bit_map_origin, bit_map_merged):
    return [x & y for x, y in zip(bit_map_origin, bit_map_merged)]


def S_step(bit_map_origin, bit_map_merged):
    index = -1
    for i in range(len(bit_map_origin)):
        if bit_map_origin[i] == 1:
            index = i
            break
    for i in range(index + 1):
        bit_map_origin[i] = 0
    for i in range(index + 1, len(bit_map_origin)):
        bit_map_origin[i] = 1

    return [x & y for x, y in zip(bit_map_origin, bit_map_merged)]


def DFS_Pruning(n, S, I):
    S_temp = []
    I_temp = []

    # add the candidate into the node sub nodes
    for i in S:
        c_s = calculate_support(S_step(n.bit_map, bitmaps[i]), 4, 3)
        if c_s > support:
            S_temp.append(i)

        # if calculate_support(S_step(n.bit_map, bitmaps[i]), 4, 3) > support:
        #     S_temp.append(i)

    for i in S_temp:
        s_greater_than_i = []
        if i != S_temp[-1]:
            s_greater_than_i = S_temp[S_temp.index(i) + 1:]
        # new the node when recursive call DFS function
        # DFS_Pruning(S_step(n.bit_map, bitmaps[i]), S_temp, s_greater_than_i)
        DFS_Pruning(TreeNode('', S_step(n.bit_map, bitmaps[i]), []), S_temp, s_greater_than_i)


    for i in I:
        # 4, 3 = bitmap numbers, customer numbers
        if calculate_support([x & y for x, y in zip(n.bit_map, bitmaps[i])], 4, 3) > support:
            I_temp.append(i)

    for i in I_temp:
        # all elements in I-temp greater than i
        i_greater_than_i = []
        if i != I_temp[-1]:
            i_greater_than_i = I_temp[I_temp.index(i) + 1:]

        DFS_Pruning(I_step(n.bit_map, bitmaps[i]), S_temp, i_greater_than_i)


root = TreeNode('null', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [])
DFS_Pruning(root, S, I)


# print(bitmaps[0])
# print(bitmaps[1])