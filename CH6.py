import fractions


def addFP(p, P1, P2, Q1, Q2, A=1):
    # (P1, P2) \oplus (Q1, Q2) over F_p
    # on the curve Y^2 = X^3 + AX + B
    # (None, None) means the point at infinity
    if P1 == Q1 and P2 + Q2 == p:
        return None, None
    if P1 is P2 is None:
        if Q1 is Q2 is None:
            return None
        else:
            return Q1, Q2
    if Q1 is Q2 is None:
        return P1, P2
    if P1 == Q1 and P2 == Q2:
        slope = ((3*(P1**2) + A) * (inv(2*P2, p))) % p
    else:
        slope = ((Q2-P2) * (inv(Q1-P1, p))) % p
    nu = (P2 - slope * P1) % p
    R1 = (slope * slope - Q1 - P1) % p
    R2 = (-(slope * R1 + nu)) % p
    return R1, R2


def find_points(p, A, B):
    # finds points in Y^2 = X^3 + AX + B over F_p
    points = [(None, None)]
    for x in range(0, p):
        right_side = (x**3 + A*x + B) % p
        ls = legendre_symbol(right_side, p)
        if ls in [0, 1]:
            for y in range(0, int((p+1)/2)):
                if y**2 % p == right_side:
                    points.append((x, y))
                    if ls == 1:
                        points.append((x, p-y))
                    break
    return points, len(points)


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


def legendre_symbol(a, p):
    # using euler's criterion
    ls = pow(a, int((p - 1) / 2), p)
    if ls == p - 1:
        return -1
    else:
        return ls


def double_and_add(n, a, b, N, A):
    # P = (a, b)
    # calculates nP mod N
    P = (a, b)
    Q = P
    R = (None, None)
    while n > 0:
        if n % 2 == 1:
            try:
                R = addFP(N, R[0], R[1], Q[0], Q[1], A)
            except TypeError:
                return fractions.gcd((Q[0]-R[0]) % N, N)
        Q = addFP(N, Q[0], Q[1], Q[0], Q[1], A)
        n = int(n/2)
    return R


def lenstra_factor(N, a, b, A):
    P = (a, b)
    B = (b**2 - a**3 - A*a) % N
    for j in range(2, 100):
        P = double_and_add(j, P[0], P[1], N, A)
        if isinstance(P, int):
            if P < N:
                return 'A factor of ' + str(N) + ' is ' + str(P)
            else:
                return 'failed'

print(lenstra_factor(589,2,5,4))
print(lenstra_factor(26167,2,12,4))
print(lenstra_factor(1386493,1,1,3))
print(lenstra_factor(28102844557,7,4,18))

