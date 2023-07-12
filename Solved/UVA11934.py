"""
Complete the problem on UVa
"""
def solution(a, b, c, d, L):
    count = 0
    for x in range(L + 1):
        if (a*x**2 + b*x + c) % d == 0:
            count += 1
    return count


while 1:
    inp = input()
    if inp == '0 0 0 0 0':
        break
    a, b, c, d, L = [int(x) for x in inp.split()]
    print(solution(a, b, c, d, L))