def HUI_Miner(P_UL, UL, minutil):
    for i in range(len(UL)):
        print(UL[i])

        exULs = []
        for j in range(i+1, len(UL)):
            exULs.append(P_UL + UL[i][-1] + UL[j][-1])
        HUI_Miner(UL[i], exULs, minutil)

HUI_Miner('', ['e', 'c', 'b', 'a', 'd'], 20)
