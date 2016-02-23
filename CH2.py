import math


def dlog(g, h, p):
    """ calculates the discrete logarithm

    :param g: the base
    :param h: the power of g modulo p
    :param p: the modulus
    :return: x in g^x = h (mod p)
    """
    g_powers = [1]
    for x in range(1, p):
        if g_powers[-1] == h:
            return x-1
        g_powers.append((g_powers[x-1]*g) % p)
    return 'undefined'


def dlog_shank(g, h, p, order=None):
    """ calculates the discrete logarithm using
    the Shank's Babystep-Giantstep Algorithm

    :param g: the base
    :param h: the power of g modulo p
    :param p: the modulus
    :param order: order of g modulo p
    :return: x in g^x = h (mod p)
    """
    if order is None:
        order = p
    n = 1 + math.floor(math.sqrt(order))
    u = pow(inv(g, p), n, p)
    list1 = [pow(g, x, p) for x in range(0, n+1)]
    list2 = [h*pow(u, x, p) % p for x in range(0, n+1)]
    for i in range(0, n+1):
        for j in range(0, n+1):
            if list1[i] == list2[j]:
                return i + j*n
    return 'undefined'


def dlog_pohlig(g, h, p, n_factors=None):
    """ calculates the discrete logarithm using
    the Pohlig-Hellman Algorithm

    :param g: the base
    :param h: the power of g modulo p
    :param p: the modulus
    :param n_factors: dictionary of {prime factor: power}
    :return: x in g^x = h (mod p)
    """
    n = p-1
    y_i = []
    if n_factors is None:
        n_factors = factor(n)
    for prime in n_factors:
        order = prime**n_factors[prime]
        power = int(n/order)
        y_i.append((dlog_shank(pow(g, power, p), pow(h, power, p), p, order), order))
    return chinese_remainder(y_i)


def factor(n):
    """ factors a positive integer using trial division

    :param n: integer to be positive
    :return: dictionary with pairs in the form
            of prime factor:power
    """
    factors = {}
    maxi = math.floor(math.sqrt(n)/2)
    while n/2 == int(n/2):
        if 2 not in factors:
            factors[2] = 0
        factors[2] += 1
        n /= 2
    for x in range(1, maxi+1):
        p = 2*x+1
        while n/p == int(n/p):
            if p not in factors:
                factors[p] = 0
            factors[p] += 1
            n /= p
            if n == 1:
                return factors
    if n != 1:
        factors[int(n)] = 1
    return factors


def chinese_remainder(inp):
    """ solves a system of congruencies

    :param inp: list of tuples (k, n)
                meaning x = k (mod n)
    :return: value that solves every congruency
    """
    ans = inp[0][0]
    prod = inp[0][1]
    while len(inp) > 1:
        k = inp[1][0]
        n = inp[1][1]
        x = cong_solve(prod, k-ans, n)
        ans += prod * x
        prod *= n
        del inp[0]
    return ans


def cong_solve(a, b, n):
    """ solves the congruence ax = b (mod n)

    :param a: coefficient of x
    :param b: right side of congruency
    :param n: modulus
    :return: the value of x (mod n)
    """
    x = inv(a, n) * b % n
    return x


def inv(a, n):
    """ calculates the inverse of a modulo n

    :param a: the number whose inverse is to be taken
    :param n: modulus
    :return: inverse of a modulo n
    """
    u, g, x, y = 1, a, 0, n
    while y != 0:
        q = int(g/y)
        s = u - q*x
        t = g % y
        u, g = x, y
        x, y = s, t
    if g != 1:
        return 'undefined'
    if u < 0 or u >= n/g:
        u %= int(n/g)
    return u


def list_powers(a, b):
    """ working with F_7[x]/(x^2+1)
        lists powers of ax + b

    :param a: coefficient of the linear term
    :param b: constant
    :return: list of powers of ax + b in (a, b)
    """
    powers = [(a, b)]
    for power in range(2, 49):
        a_prev = powers[power-2][0]
        b_prev = powers[power-2][1]
        powers.append(((a*b_prev + b*a_prev) % 7, (b*b_prev-a*a_prev) % 7))
    return powers
