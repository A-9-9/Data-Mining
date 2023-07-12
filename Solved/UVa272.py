def solution(s, t):
    ret = ''
    for i in s:
        if i == '"':
            if t == 0:
                t = 1
                ret += '``'
            else:
                t = 0
                ret += "''"
        else:
            ret += i
    print(ret)
    return t


temp = 0
while 1:
    try:
        temp = solution(input(), temp)
    except EOFError:
        break