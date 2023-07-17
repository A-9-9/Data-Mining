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
maximum_size_of_sequence = 3
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
    global count
    # Limit sequence size and detect if the node is root or not on recursive function.
    if n.bit_map is not None and len(n.val) > maximum_size_of_sequence:
        return
    S_temp = []
    # S_temp_nodes = []
    I_temp = []
    I_temp_nodes = []

    print(n.val)
    # print(n.bit_map)
    # Exclusion root node
    if n.bit_map is not None:
        print(calculate_support(n.bit_map, 4, 3))
    print('=' * 20)

    '''
    Add an item in the item set S by measuring whether the item is a high-frequency value.
    While the current node is a root, then set the bitmap with a specific item, 
    otherwise, do the s-step to merge both two bitmaps and calculate absolute support.
    
    Compare the sequence frequency, then identify whether the current node is root or not, 
    creating a new node with a specific item and bitmap.
    
    Recursive the DFS function by traversing s-temp
    '''
    for i in S:
        if n.bit_map is None:
            c_s = calculate_support(bitmaps[i], 4, 3)
        else:
            merged_bitmap = S_step(copy.copy(n.bit_map), bitmaps[i], 4)
            c_s = calculate_support(merged_bitmap, 4, 3)

        if c_s > support:
            S_temp.append(i)
            if n.bit_map is None:
                S_sud_node = TreeNode([items[i]], bitmaps[i], [])
            else:
                sud = copy.copy(n.val)
                sud.append(items[i])
                S_sud_node = TreeNode(sud, merged_bitmap, [])

            n.sub_nodes.append(S_sud_node)

    for i in range(len(S_temp)):
        s_greater_than_i = []
        if S_temp[i] != S_temp[-1]:
            s_greater_than_i = S_temp[i + 1:]

        DFS_Pruning(n.sub_nodes[i], S_temp, s_greater_than_i)

    for i in I:
        # Error occurs without adding this condition, but total sequence numbers are the same.
        if n.bit_map is None:
            break

        merged_bitmap_I = I_step(copy.copy(n.bit_map), bitmaps[i])
        if calculate_support(merged_bitmap_I, 4, 3) > support:
            I_temp.append(i)
            sud = copy.copy(n.val)
            sud[-1] += ',%s' % (items[i])
            I_sud_node = TreeNode(sud, merged_bitmap_I, [])
            I_temp_nodes.append(I_sud_node)
            # could separate the sub-nodes into S-sub-nodes and I-sub-nodes from the tree structure,
            # and remove the relative data like S_temp_nodes and I_temp_nodes
            # n.sub_nodes.append(I_sud_node)

    for i in range(len(I_temp)):
        i_greater_than_i = []
        if I_temp[i] != I_temp[-1]:
            i_greater_than_i = I_temp[i + 1:]

        DFS_Pruning(I_temp_nodes[i], S_temp, i_greater_than_i)


# count = 0
root = TreeNode('null', None, [])
DFS_Pruning(root, S, I)
# print(count)

