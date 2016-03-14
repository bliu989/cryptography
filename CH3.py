import math


def lucas_lehmer(k):
    for n in range(math.floor(k / 2), 1000000):
        n = 2 * n + 1
        m_n = 2 ** n - 1
        s_i = 4
        if (n - 1) % 100 == 0:
            print(n)
        for i in range(n - 2):
            s_i = (s_i ** 2 - 2) % m_n
        if s_i == 0:
            print(n, m_n)


def miller_rabin(n):
    k = 0
    temp = n - 1
    while temp % 2 == 0:
        temp /= 2
        k += 1
    q = int((n - 1) / 2 ** k)
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        message = miller_rabin_witness_test(a, n, q, k)
        if message == "Composite. Witness: " or message == "Definitely Composite. Witness: ":
            print(message + str(a))
            break
        print(message + str(a))


def miller_rabin_witness_test(a, n, q, k):
    if gcd(a, n) > 1:
        return "Definitely Composite. Witness: "
    a = (a ** q) % n
    if a % n == 1:
        return "Non-Witness: "
    for i in range(0, k):
        if a % n == n - 1:
            return "Non-Witness: "
        a = (a ** 2) % n
    return "Composite. Witness: "


def gcd(a, b):
    u, g, x, y = 1, a, 0, b
    while y != 0:
        q = int(g / y)
        s = u - q * x
        t = g % y
        u, g = x, y
        x, y = s, t
    if u < 0 or u >= b / g:
        u %= int(b / g)
    return g
