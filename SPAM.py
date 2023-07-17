"""
Data: CID, TID, Item
(1) Pruning candidate from Sn(s-extensions).
(2) Recursively doing S-step(sequence-extension step) with specific Sn.
(3) Pruning candidate from In(i-extensions).
(4) Recursively doing I-step(itemset-extension step) with specific In.
"""
import copy

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
support = 0
bitmaps = [
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]
S = [0, 1, 2, 3]
I = [0, 1, 2, 3]
items = ['a', 'b', 'c', 'd']

# Definition for Lexicographic tree node.
class TreeNode:
    def __init__(self, val, bit_map, sub_nodes):
        self.val = val
        self.bit_map = bit_map
        self.sub_nodes = sub_nodes


def I_step(bit_map_origin, bit_map_merged):
    return [x & y for x, y in zip(bit_map_origin, bit_map_merged)]


def S_step(bit_map_origin, bit_map_merged, bit_size):
    li2 = []
    for i in range(0, len(bit_map_origin), bit_size):
        li = copy.copy(bit_map_origin[i: i + bit_size])
        found_one = False
        for i in range(len(li)):
            if found_one:
                li[i] = 1

            if li[i] == 1 and not found_one:
                found_one = True
                li[i] = 0
        li2.extend(li)

    return [x & y for x, y in zip(li2, bit_map_merged)]


def DFS_Pruning(n, S, I):
    if n.bit_map != None and len(n.val) > 3:
        return
    S_temp = []
    S_temp_nodes = []
    I_temp = []
    I_temp_nodes = []

    print(n.val)
    print(n.bit_map)
    if n.bit_map != None:
        print(calculate_support(n.bit_map, 4, 3))
    print('='*20)
    # add the candidate into the node sub nodes
    for i in S:
        # c_s = calculate_support(S_step(n.bit_map, bitmaps[i]), 4, 3)

        # if using sets of all 1 in root set, there were be an error while doing s-step transform
        if n.bit_map == None:
            c_s = calculate_support(bitmaps[i], 4, 3)
        else:
            sud_bitmap = S_step(copy.copy(n.bit_map), bitmaps[i], 4)
            c_s = calculate_support(sud_bitmap, 4, 3)
            pass

        if c_s > support:
            S_temp.append(i)

            # new a new node when the new sequence is frequent
            if n.bit_map == None:
                S_sud_node = TreeNode([items[i]], bitmaps[i], [])
            else:
                sud = copy.copy(n.val)
                sud.append(items[i])

                S_sud_node = TreeNode(sud, sud_bitmap, [])

            n.sub_nodes.append(S_sud_node)
            S_temp_nodes.append(S_sud_node)


    for i in range(len(S_temp)):
        s_greater_than_i = []
        if S_temp[i] != S_temp[-1]:
            s_greater_than_i = S_temp[i + 1:]

        DFS_Pruning(S_temp_nodes[i], S_temp, s_greater_than_i)

    # for i in S_temp:
    #     s_greater_than_i = []
    #     if i != S_temp[-1]:
    #         s_greater_than_i = S_temp[S_temp.index(i) + 1:]

        # new the node when recursive call DFS function
        # DFS_Pruning(S_step(n.bit_map, bitmaps[i]), S_temp, s_greater_than_i)
        # DFS_Pruning(TreeNode('', S_step(n.bit_map, bitmaps[i]), []), S_temp, s_greater_than_i)


    # for i in I:
    #     # 4, 3 = bitmap numbers, customer numbers
    #     if calculate_support([x & y for x, y in zip(n.bit_map, bitmaps[i])], 4, 3) > support:
    #         I_temp.append(i)
    #
    # for i in I_temp:
    #     # all elements in I-temp greater than i
    #     i_greater_than_i = []
    #     if i != I_temp[-1]:
    #         i_greater_than_i = I_temp[I_temp.index(i) + 1:]
    #
    #     DFS_Pruning(I_step(n.bit_map, bitmaps[i]), S_temp, i_greater_than_i)


root = TreeNode('null', None, [])
DFS_Pruning(root, S, I)


# print(bitmaps[0])
# print(bitmaps[1])