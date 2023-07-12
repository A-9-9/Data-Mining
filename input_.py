import math

data = []
# input data from the file
while 1:
    try:
        sud = [int(x) for x in input().split()]
        data.append(sud)
    except EOFError:
        break


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
