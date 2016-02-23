import math

# calculates the discrete logarithm base g
# of h modulo p
def dlog(g, h, p):
    gPowers = [1]
    for x in range(1, p):
        if gPowers[-1] == h:
            return x-1
        gPowers.append((gPowers[x-1]*g)%p)
    return 'undefined'

# calculates the discrete logarithm base g
# of h modulo p using Shank's babystep-
# giantstep method
def dlog_shank(g, h, p, order = None):
    if order == None:
        order = p
    n = 1 + math.floor(math.sqrt(order))
    u = pow(inv(g,p), n, p)
    list1 = [pow(g, x, p) for x in range(0,n+1)]
    list2 = [h*pow(u, x, p) % p for x in range(0,n+1)]
    for i in range(0,n+1):
        for j in range(0,n+1):
            if list1[i] == list2[j]:
                return i + j*n
    return 'undefined'

# calculates the discrete logarithm base g
# of h modulo p using the Pohlig-Hellman
# algorithm
# optional input is a dictionary of prime factors
# with their powers as values
def dlog_pohlig(g ,h, p, N_factors = None):
    N = p-1
    y_i = []
    if N_factors == None:
        N_factors = factor(N)
    for prime in N_factors:
        order = prime**N_factors[prime]
        power = int(N/order)
        y_i.append((dlog_shank(pow(g, power, p), pow(h, power, p), p, order), order))
    return chinese_remainder(y_i)

# returns a dictionary of primes factors with
# the primes being the key and its power being
# the value by using trial division
def factor(n):
    factors = {}
    max = math.floor(math.sqrt(n)/2)
    while n/2 == int(n/2):
        if 2 not in factors:
            factors[2] = 0
        factors[2] += 1
        n = n/2
    for x in range(1, max+1):
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

# takes a list of tuples with each tuple (k,n)
# meaning that x = k (mod n) and solves the
# system of congruences
def chinese_remainder(inp):
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

# solves the congruence ax = b (mod n)
def cong_solve(a, b, n):
    x = inv(a,n) * b % n
    return x

# inverse of a modulo n
def inv(a,n):
    u, g, x, y = 1, a, 0, n
    while y != 0:
        q = int(g/y)
        s = u - q*x
        t = g%y
        u, g = x, y
        x, y = s, t
    if g != 1:
        return 'undefined'
    if u < 0 or u >= n/g:
        u = u%int(n/g)
    return u

# working with F_7[x]/(x^2+1)
# lists powers of ax + b
def list_powers(a, b):
    powers = [(a, b)]
    for power in range(2, 49):
        a_prev = powers[power-2][0]
        b_prev = powers[power-2][1]
        powers.append(((a*b_prev + b*a_prev)%7,(b*b_prev-a*a_prev)%7))
    return powers
