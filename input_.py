import math

data = []
# input data from the file

# while 1:
#     try:
#         sud = [int(x) for x in input().split()]
#         data.append(sud)
#     except EOFError:
#         break

with open('test.txt') as f:
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
bit_size = -1
sud = {}
for customer, transaction, item in data:
    cus_num = max(cus_num, customer)
    item_num = max(item_num, item)
    if not customer in sud:
        sud[customer] = [(customer, transaction)]
    else:
        if not (customer, transaction) in sud[customer]:
            sud[customer].append((customer, transaction))

for i in sud.values():
    bit_size = max(bit_size, len(i))

bit_size = 2 ** math.ceil(math.log(bit_size, 2))

# Undo: create bitmap with above parameter
bit_map = [[0 for bit in range(cus_num*bit_size)] for item in range(item_num)]

# calculate item set group by each transaction
dic = {}
for i in data:
    if (i[0], i[1]) not in dic:
        dic[(i[0], i[1])] = [i[2]]
    else:
        dic[(i[0], i[1])].append(i[2])

# generate bitmap according to transaction
count = 0
cus = data[0][0]
for k, v in dic.items():
    if cus != k[0]:
        cus = k[0]
        while count % bit_size != 0:
            count += 1
    for i in v:
        bit_map[i - 1][count] = 1

    count += 1

def calculate_support(item_bit_map, bit_size, cus_num):
    support = 0
    for i in range(cus_num):
        # print(item_bit_map[bit_size*i:bit_size*(i+1)])
        if 1 in item_bit_map[bit_size * i:bit_size * (i + 1)]:
            support += 1
    return support









