def addFP(p, P1, P2, Q1, Q2, A=1):
    # (P1, P2) \oplus (Q1, Q2) over F_p
    # on the curve Y^2 = X^3 + AX + B
    # (0,0) means the point at infinity
    if P1 == Q1 and P2 + Q2 == p:
        return 0, 0
    if P1 == P2 == 0:
        if Q1 == Q2 == 0:
            return 0, 0
        else:
            return Q1, Q2
    if Q1 == Q2 == 0:
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
    points = [(0, 0)]
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
