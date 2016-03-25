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


def factor(k, N, b):
    """
    factors N by seeing if kN + b^2 is a perfect square
    :param k:
    :param N:
    :param b:
    :return:
    """
    while (math.sqrt(k*N + b**2)) % 1 != 0:
        b += 1
    a = int(math.sqrt(k*N + b**2))
    factor1 = gcd(N, a + b)
    factor2 = gcd(N, a - b)
    return factor1, factor2

def psi(X, B):
    """
    number of B-smooth numbers between 2 and X
    :param X:
    :param B:
    :return:
    """
    count = 0
    primes = [x for x in [2, 3, 5, 7] if x <= B]
    if B > 7:
        return "not supported"
    for x in range(2, X+1):
        for prime in primes:
            while x % prime == 0:
                x /= prime
        if x < B:
            count += 1
    return count


def quadratic_sieve_illustrate(N, B, lower, upper):
    """
    illustrates the quadratic sieve for N using prime powers up to B
    using values from F(lower) to F(upper), where F(T) = T^2 - N

    the way that this function generates and uses prime powers
    is not efficient
    :param N:
    :param B:
    :param lower:
    :param upper:
    :return:
    """
    if B > 16:
        return "not supported"
    primes = [2, 3, 5, 7, 11, 13]
    prime_powers = generate_prime_powers(B)
    values = [t**2 - N for t in range(lower, upper + 1)]
    print()
    print(list_to_string([t for t in range(lower, upper+1)], 5))
    print(list_to_string(values, 5))
    for prime_power in prime_powers:
        sieve_arrows = []
        solutions = []  # solutions to t^2 = N (mod p^e)
        n = N % prime_power
        base_prime = prime_power
        for prime in primes:
            if prime_power % prime == 0:
                base_prime = prime
                break
        for t in range(1, prime_power):
            if t**2 % prime_power == n:
                solutions.append(t)
        if len(solutions) != 0:
            for x in range(lower, upper + 1):
                if (x % prime_power) in solutions:
                    sieve_arrows.append("↓" + str(prime_power))
                    values[x-lower] = int(values[x-lower]/prime)
                else:
                    sieve_arrows.append("")
            print(list_to_string(sieve_arrows, 5))
            print(list_to_string(values, 5))


def list_to_string(lst, length):
    return_string = ""
    for item in lst:
        return_string += str(item).rjust(length)
    return return_string


def generate_prime_powers(B):
    primes = [2, 3, 5, 7, 11, 13]
    if B > 16:
        return "not supported"
    prime_powers = []
    index = 0
    while primes[index] <= B:
        p = primes[index]
        while p <= B:
            prime_powers.append(p)
            p *= primes[index]
        if index < len(primes)-1:
            index += 1
        else:
            break
    prime_powers.sort()
    return prime_powers
