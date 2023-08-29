def HUI_Miner(P_UL, UL, minutil):
    for i in range(len(UL)):
        print(UL[i])

        exULs = []
        for j in range(i + 1, len(UL)):
            exULs.append(P_UL + UL[i][-1] + UL[j][-1])
        HUI_Miner(UL[i], exULs, minutil)


# HUI_Miner('', ['e', 'c', 'b', 'a', 'd'], 20)


# Database
utility_table = {'a': 1, 'b': 2, 'c': 1, 'd': 5, 'e': 4, 'f': 3, 'g': 1}
transaction_table = [
    [['b', 'c', 'd', 'g'], [1, 2, 1, 1]],
    [['a', 'b', 'c', 'd', 'e'], [4, 1, 3, 1, 1]],
    [['a', 'c', 'd'], [4, 2, 1]],
    [['c', 'e', 'f'], [2, 1, 1]],
    [['a', 'b', 'd', 'e'], [5, 2, 1, 2]],
    [['a', 'b', 'c', 'f'], [3, 4, 1, 2]],
    [['d', 'g'], [1, 5]],
]

minutil = 30

# Data preprocess -> transform data
transaction_table_transformed = []
for i in transaction_table:
    transaction_table_transformed.append([list(x) for x in zip(i[0], i[1])])

utility_list = list(utility_table.keys())
twu = {}
for i in utility_list:
    sud = 0
    for j in transaction_table:
        if i in j[0]:
            for k in range(len(j[0])):
                 sud += j[1][k] * utility_table[j[0][k]]
    twu[i] = sud

# prune items according to Property01
twu = {k: v for k, v in twu.items() if v >= minutil}
# sort items by twu
twu = sorted(twu.items(), key=lambda x: x[1])
twu = {x[0]: x[1] for x in twu}
utility_list_transformed = [x for x in twu.keys()]

# Second time scan database
# Remove items by property01 in database
for i in transaction_table_transformed:
    for j in range(len(i)):
        if i[j][0] not in twu.keys():
            del i[j]

# Sort items in twu-ascending order
sud = []
for i in transaction_table_transformed:
    sud.append(sorted(i, key=lambda x: twu[x[0]]))

transaction_table_transformed = sud

# Merged utility in transaction
for i in transaction_table_transformed:
    for j in i:
        j[1] *= utility_table[j[0]]

print(transaction_table_transformed)
print(utility_list_transformed)
for item in utility_list_transformed:
    print('='*5 + item + '='*5)
    for transaction in range(len(transaction_table_transformed)):
        E = []
        for items_index in range(len(transaction_table_transformed[transaction])):
            if transaction_table_transformed[transaction][items_index][0] == item:
                # save item in data structure
                E = [transaction + 1, transaction_table_transformed[transaction][items_index][1], sum([x[1] for x in transaction_table_transformed[transaction][items_index + 1:]])]
                print(E)
                continue


'''
# HUI Miner steps:
(1) Initial Utility-List
1. First scan database: Calculate twu and pruned item if the item's twu less then minimum utilities by Property01
   and then sort item by item's twu-ascending order.
2. Second scan database: Create revised database by: all the item must belongs to remaining items(First step) in 
   transaction, the remaining items are sorted in twu-ascending order.
3. Initial Utility-List: contains fields (tid, iutil, rutil).

(2) Construct Algorithm(P, Px, Py) return (Pxy)
(3) HUI-Miner algorithm(P, ULs, minutil)
(4) Given a database and minimum utilities, after construct initial Utility-List, 
    HUI-Miner(∅, IULS, minutil) can mine all HUI
'''
