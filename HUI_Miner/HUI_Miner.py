"""
# HUI Miner steps:
(1) Initial Utility-List
1. First scan database: Calculate twu and pruned item if the item's twu less than minimum utilities by Property01
   and then sort item by item's twu-ascending order.
2. Second scan database: Create revised database by: all the item must belongs to remaining items(First step) in
   transaction, the remaining items are sorted in twu-ascending order.
3. Initial Utility-List: contains fields (tid, iutil, rutil).

(2) Construct Algorithm(P, Px, Py) return (Pxy)
(3) HUI-Miner algorithm(P, ULs, minutil)
(4) Given a database and minimum utilities, after construct initial Utility-List,
    HUI-Miner(∅, IULS, minutil) can mine all HUI
"""
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

# print(transaction_table_transformed)
# print(utility_list_transformed)
class UtilityList:
    def __init__(self, item, UL):
        self.item = item
        self.UL = UL
        pass

IUL_Obj = []
IUL = []
for item in utility_list_transformed:
    E = []
    for transaction in range(len(transaction_table_transformed)):
        for items_index in range(len(transaction_table_transformed[transaction])):
            if transaction_table_transformed[transaction][items_index][0] == item:
                # save item in utility-list

                E.append([transaction + 1, transaction_table_transformed[transaction][items_index][1], sum([x[1] for x in transaction_table_transformed[transaction][items_index + 1:]])])
                continue
    IUL_Obj.append(UtilityList(item, E))
    IUL.append(E)


def Construct(P_UL, Px_UL, Py_UL):
    Pxy_UL = []
    Ex_index = 0
    Ey_index = 0
    while Ex_index < len(Px_UL) and Ey_index < len(Py_UL):
        if Px_UL[Ex_index][0] == Py_UL[Ey_index][0]:
            Exy = []
            if P_UL is not None:
                for E in range(len(P_UL)):
                    if P_UL[E][0] == Px_UL[Ex_index][0]:
                        Exy = [Px_UL[Ex_index][0], Px_UL[Ex_index][1] + Py_UL[Ey_index][1] - P_UL[E][1], Py_UL[Ey_index][2]]
            else:
                Exy = [Px_UL[Ex_index][0], Px_UL[Ex_index][1]+Py_UL[Ey_index][1], Py_UL[Ey_index][2]]
            Pxy_UL.append(Exy)
            Ex_index += 1
            Ey_index += 1
        else:
            if Px_UL[Ex_index][0] > Py_UL[Ey_index][0]:
                Ey_index += 1
            else:
                Ex_index += 1
    return Pxy_UL


def HUI_Miner(P, ULs, minutil):
    for X in ULs:
        # print(X.item)
        if sum([x[1] for x in X.UL]) >= minutil:
            print(X.item, "Utility:", sum([x[1] for x in X.UL]))

        if sum([x[1] for x in X.UL]) + sum([x[2] for x in X.UL]) >= minutil:
            exULs = []
            for Y in ULs[ULs.index(X)+1:]:
                # UtilityList(X + Y[-1], Construct(P.UL, X.UL, Y.UL))
                # print(P.item, X.item, Y.item)
                exULs.append(UtilityList(X.item + Y.item[-1], Construct(P.UL, X.UL, Y.UL)))
            HUI_Miner(X, exULs, minutil)


HUI_Miner(UtilityList('', None), IUL_Obj, 20)


