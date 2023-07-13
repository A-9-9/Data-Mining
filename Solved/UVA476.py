def in_rectangles(point, recs, count):
    temp = True
    for i in range(len(recs)):
        # print(recs[i][0], point[0], recs[i][2], recs[i][0] < point[0] < recs[i][2])
        # print(recs[i][1], point[1], recs[i][3], recs[i][1] < point[1] < recs[i][3])
        if recs[i][0] < point[0] < recs[i][2] and recs[i][3] < point[1] < recs[i][1]:
            print("Point %s is contained in figure %s" % (count, i+1))
            temp = False

    if temp:
        print("Point %s is not contained in any figure" % (count))


recs = []
point_count = 1
while 1:
    try:
        s = [x for x in input().split()]
        if s[0] == 'r':
            # print([float(x) for x in s[1:]])
            recs.append([float(x) for x in s[1:]])
        elif s[0] != '*' and s[0] != '9999.9' and s[1] != '9999.9':
            # print([float(x) for x in s])
            in_rectangles([float(x) for x in s], recs, point_count)
            point_count += 1
            pass
        pass

    except EOFError:
        # print(recs)
        break