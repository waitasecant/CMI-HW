# Himanshu, MDS202327

# 1
def delchar(s, c):
    if len(c) > 1:
        return s
    else:
        news = ""
        for i in s:
            if i != c:
                news = news + i
        return news


# 2
def nestingdepth(s):
    l = ""
    for i in s:
        if i in ["(", ")"]:
            l = l + i
    tstr = "()"
    count = 0
    if l == "":
        return 0
    while l != "":
        if tstr not in l:
            return -1
        else:
            l = l.replace(tstr, "", -1)
            count = count + 1
    return count


# 3
def odd(x):
    if x % 2 == 0:
        return "0"
    else:
        return "1"


def notodd(x):
    if x % 2 == 0:
        return "1"
    else:
        return "0"


def accordian(l):
    newl = []
    for i in range(len(l)):
        if i < len(l)-1:
            newl.append(abs(l[i]-l[i+1]))

    newlstr = ""
    for i in range(len(newl)):
        if i < len(newl)-1:
            if newl[i]-newl[i+1] < 0:
                newlstr = newlstr + "1"
            elif newl[i]-newl[i+1] > 0:
                newlstr = newlstr + "0"
            else:
                return False

    test0, test1 = "", ""
    for i in range(len(newl)-1):
        test0 = test0 + odd(i)
        test1 = test1 + notodd(i)
    print(newl, newlstr)
    if newlstr in [test0, test1]:
        return True
    else:
        return False


# 4
def rotate(l):
    newl = []
    for i in range(len(l[0])):
        sl = []
        for j in l[::-1]:
            sl.append(j[i])
        newl.append(sl)
    return newl
