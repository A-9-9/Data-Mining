import copy
import math

# Definition for Lexicographic tree node.
class TreeNode:
    def __init__(self, val, bit_map, s_sub_nodes, i_sub_nodes):
        self.val = val
        self.bit_map = bit_map
        self.s_sub_nodes = s_sub_nodes
        self.i_sub_nodes = i_sub_nodes


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


"""
# Calculate support according to relative bitmap.
# First, split the bitmap by customer number, each customer has a specific size of the bitmap, 
# thus we could count their support.
"""
def calculate_support(item_bit_map, bit_size, cus_num):
    support = 0
    for i in range(cus_num):
        if 1 in item_bit_map[bit_size * i:bit_size * (i + 1)]:
            support += 1
    return support


def DFS_Pruning(n, S, I):
    global recursive_instructions_count
    # Limit sequence size and detect if the node is root or not on recursive function.
    if n.bit_map is not None and len(n.val) > maximum_size_of_sequence:
        return
    S_temp = []
    I_temp = []

    print(n.val)
    print(n.bit_map)
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
                S_sud_node = TreeNode([items[i]], bitmaps[i], [], [])
            else:
                sud = copy.copy(n.val)
                sud.append(items[i])
                S_sud_node = TreeNode(sud, merged_bitmap, [], [])

            n.s_sub_nodes.append(S_sud_node)

    for i in range(len(S_temp)):
        s_greater_than_i = []
        if S_temp[i] != S_temp[-1]:
            s_greater_than_i = S_temp[i + 1:]
        recursive_instructions_count += 1
        DFS_Pruning(n.s_sub_nodes[i], S_temp, s_greater_than_i)

    for i in I:
        # Error occurs without adding this condition, but total sequence numbers are the same.
        if n.bit_map is None:
            break

        merged_bitmap_I = I_step(copy.copy(n.bit_map), bitmaps[i])
        if calculate_support(merged_bitmap_I, 4, 3) > support:
            I_temp.append(i)
            sud = copy.copy(n.val)
            sud[-1] += ',%s' % (items[i])
            I_sud_node = TreeNode(sud, merged_bitmap_I, [], [])
            n.i_sub_nodes.append(I_sud_node)

    for i in range(len(I_temp)):
        i_greater_than_i = []
        if I_temp[i] != I_temp[-1]:
            i_greater_than_i = I_temp[i + 1:]
        recursive_instructions_count += 1
        DFS_Pruning(n.i_sub_nodes[i], S_temp, i_greater_than_i)


# input data from text file
data = []
with open('test.txt') as f:
    for i in f.readlines():
        sud = [int(x) for x in i.split()]
        data.append(sud)

"""
--------------------Data preprocessing--------------------
# Input data definition: CID, TID, Item
# customer_numbers: number of customers.
# item_numbers: number of items.
# bit_size: bit map size that according to the maximum size of sequences.
----------------------------------------------------------
"""
customer_numbers = -1
item_numbers = -1
bit_size = -1

sud = {}
for customer, transaction, item in data:
    customer_numbers = max(customer_numbers, customer)
    item_numbers = max(item_numbers, item)
    if customer not in sud:
        sud[customer] = [(customer, transaction)]
    else:
        if not (customer, transaction) in sud[customer]:
            sud[customer].append((customer, transaction))

for i in sud.values():
    bit_size = max(bit_size, len(i))

bit_size = 2 ** math.ceil(math.log(bit_size, 2))
bitmaps = [[0 for bit in range(customer_numbers * bit_size)] for item in range(item_numbers)]

# Calculate item set group by customers and transactions
dic = {}
for i in data:
    if (i[0], i[1]) not in dic:
        dic[(i[0], i[1])] = [i[2]]
    else:
        dic[(i[0], i[1])].append(i[2])

# Generate bitmap according to transaction and map with customer, and calculate the maximum size of sequence.
count = 0
cus = data[0][0]
maximum_size_of_sequence = -1
temporary_sequence_count = 0
for k, v in dic.items():
    # check if customer changed
    if cus != k[0]:
        cus = k[0]
        # if customer changed, fill up bitmap and switch to the next customer
        while count % bit_size != 0:
            count += 1

        maximum_size_of_sequence = max(maximum_size_of_sequence, temporary_sequence_count)
        sud_sequence_count = 0
    for i in v:
        # bitmap[item][transaction]
        bitmaps[i - 1][count] = 1

    temporary_sequence_count += 1
    count += 1

"""
--------------------Parameter definition--------------------
# support: support threshold.
# S: set of candidate items considered for S-step.
# I: set of candidate items considered for I-step.
# items: set of items.
------------------------------------------------------------
"""
support = 0
# Assume that all the item index is in order.
# S = [0, 1, 2, 3]
# I = [0, 1, 2, 3]
S = [x for x in range(item_numbers)]
I = [x for x in range(item_numbers)]
items = ['a', 'b', 'c', 'd']



"""
--------------------Main--------------------
"""

recursive_instructions_count = 0
root = TreeNode('null', None, [], [])
DFS_Pruning(root, S, I)
print(recursive_instructions_count)


def BFS(n):
    print("==========Level present==========")
    queue = [root]
    level = 0
    while len(queue) > 0:
        count = len(queue)
        print('Level: %s' % level)
        level += 1
        print([x.val for x in queue])
        for i in range(count):
            node = queue[0]
            for s in node.s_sub_nodes:
                if s != None:
                    queue.append(s)

            for i in node.i_sub_nodes:
                if i != None:
                    queue.append(i)
            del queue[0]


    print("==========End of present==========")


BFS(root)