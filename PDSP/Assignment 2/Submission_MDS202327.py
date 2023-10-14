def histogram(l):
    ld1 = []
    ld2 = []
    for i in set(l):
        ld1.append((l.count(i), i))
    ld1.sort()
    return [(i[1], i[0]) for i in ld1]


def onehop(l):

    d = {}
    for i in l:
        if i[0] in d:
            d[i[0]] = d[i[0]] + [i[1]]
        else:
            d[i[0]] = [i[1]]
    newl = []

    for i in d:
        for j in d[i]:
            if j in d:
                for k in d[j]:
                    if k != i:
                        newl.append((i, k))
    newl = list(set(newl))
    newl.sort()
    return newl


def rem0coeff(d):
    newd = {}
    for i, j in zip(d, d.values()):
        if j != 0:
            newd[i] = j
    return newd


def addpoly(p1, p2):
    d1 = dict([(i[1], i[0]) for i in p1])
    d2 = dict([(i[1], i[0]) for i in p2])
    d3 = dict([(i[1], i[0]) for i in p1+p2])

    d = {}
    for i in d3:
        if i in d1 and i in d2:
            d[i] = d1[i] + d2[i]
        else:
            d[i] = d3[i]

    newd = rem0coeff(d)

    newp = list(zip(newd, newd.values()))
    newp.sort(reverse=True)
    return [(i[1], i[0]) for i in newp]


def multpoly(p1, p2):
    if p1 == [] or p2 == []:
        return []
    else:
        d1 = dict([(i[1], i[0]) for i in p1])
        d2 = dict([(i[1], i[0]) for i in p2])

        d = {}
        for i in d1:
            for j in d2:
                if i+j in d:
                    d[i+j] = d[i+j] + [d1[i]*d2[j]]
                else:
                    d[i+j] = [d1[i]*d2[j]]
        d = dict([(i, sum(j)) for i, j in zip(d, d.values())])

        newd = rem0coeff(d)

        newp = list(zip(newd, newd.values()))
        newp.sort(reverse=True)
        return [(i[1], i[0]) for i in newp]
