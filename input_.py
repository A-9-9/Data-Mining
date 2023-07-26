import math

data = []
# input data from the file

# while 1:
#     try:
#         sud = [int(x) for x in input().split()]
#         data.append(sud)
#     except EOFError:
#         break

with open('data4.txt') as f:
    for i in f.readlines():
        sud = [int(x) for x in i.split()]
        data.append(sud)


"""
# calculate bitmap size using for creating bitmap
# cus_num: customer numbers
# item_num: item numbers
# bit_size: the bit map size that according to the maximum size of sequences
"""
cus_num = -1
item_num = -1
item_hash_set = set()
bit_size = -1
sud = {}
for customer, transaction, item in data:
    cus_num = max(cus_num, customer)
    item_num = max(item_num, item)
    if item not in item_hash_set:
        item_hash_set.add(item)
    if customer not in sud:
        sud[customer] = [(customer, transaction)]
    else:
        if not (customer, transaction) in sud[customer]:
            sud[customer].append((customer, transaction))

for i in sud.values():
    bit_size = max(bit_size, len(i))

bit_size = 2 ** math.ceil(math.log(bit_size, 2))

# Undo: create bitmap with above parameter
# bit_map = [[0 for bit in range(cus_num*bit_size)] for item in range(item_num)]
bit_map = [[0 for bit in range(cus_num*bit_size)] for item in range(len(item_hash_set))]
item_hash_set_sorted = {x: y for x, y in zip(sorted(item_hash_set), range(len(item_hash_set)))}

# calculate item set group by customers and transactions
dic = {}
for i in data:
    if (i[0], i[1]) not in dic:
        dic[(i[0], i[1])] = [i[2]]
    else:
        dic[(i[0], i[1])].append(i[2])

# generate bitmap according to transaction and map with customer
count = 0
sequence_count = -1
sud_sequence_count = 0
cus = data[0][0]

for k, v in dic.items():
    # check if customer changed

    if cus != k[0]:
        cus = k[0]
        # if customer changed, fill up bitmap and switch to the next customer
        while count % bit_size != 0:
            count += 1

        sequence_count = max(sequence_count, sud_sequence_count)
        sud_sequence_count = 0
    for i in v:
        # bitmap[item][transaction]
        bit_map[item_hash_set_sorted[i] - 1][count] = 1
        # bit_map[i - 1][count] = 1
    sud_sequence_count += 1
    count += 1

def calculate_support(item_bit_map, bit_size, cus_num):
    support = 0
    for i in range(cus_num):
        # print(item_bit_map[bit_size*i:bit_size*(i+1)])
        if 1 in item_bit_map[bit_size * i:bit_size * (i + 1)]:
            support += 1
    return support


# print(data)
print(item_hash_set_sorted)
# print([x for x in item_hash_set_sorted.keys()])
# print(bit_map[item_hash_set_sorted[3704]-1])
# print(len(item_hash_set))
# print(dic)
# print(sequence_count)
# print(cus_num)
# print(item_num)
# print(bit_size)
# print(sud)
# print(item_hash_set)
# print(bit_map)







