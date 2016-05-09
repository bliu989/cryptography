def knapsack_decrypt(M, S, A, B):
    a_inv = inv(A, B)
    R = [a_inv * m % B for m in M]
    S_prime = a_inv * S % B
    knapsack_subset = subset_sum_superincreasing(R, S_prime)
    ans = ""
    for i in knapsack_subset:
        ans += str(i)
    return ans


def subset_sum_superincreasing(R, sum):
    # R is a superincreasing sequence
    n = len(R)
    X = [0 for x in range(0, n)]
    for i in range(n-1, -1, -1):
        if sum >= R[i]:
            X[i] = 1
            sum -= R[i]
    return X


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


def NTRUE_encrypt(N, p, q, h, m, r):
    pr = tuple(p*x % q for x in r)
    prh = poly_quot_mult(pr, h, N, q)
    e = tuple(map(sum, zip(prh, m)))
    return e


def poly_quot_mult(P1, P2, N, m):
    # multiply polynomials P1 and P2 in the quotient ring Z[x]/(N^2 + 1) mod m
    ans = [0 for x in range(N)]
    for i in range(N):
        for j in range(N):
            k = (i+j) % N
            ans[k] += P1[i]*P2[j] % m
            ans[k] %= m
    return tuple(ans)



#print(knapsack_decrypt([5186,2779,5955,2307,6599,6771,6296,7306,4115,637],4398,4392,8387))
print(poly_quot_mult((1,1,1,0,0), (1,0,1,1,0), 5, 2))
print(poly_quot_mult((1,1,1,1,0), (1,0,1,1,0), 5, 2))
print(poly_quot_mult((2,4,4,4,0,0,2), (1,0,3,0,2,0,0), 7, 5))

print(poly_quot_mult((1,1,0,0,1), (1,0,1,1,0), 5, 2))


print(NTRUE_encrypt(7,3,29,(3,14,-4,13,-6,2,7),(1,1,-1,-1,0,0,-1),(-1,0,1,0,0,-1,1)))




