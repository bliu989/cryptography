import string, fractions
alphabet = string.ascii_lowercase

def vignere(keyword, text):
    message = ''
    length = len(keyword)

    for i in range(0, len(text)):
        message += alphabet[(alphabet.index(text[i]) - alphabet.index(keyword[i % length])) % 26]

    return message


def frequency_table(text):
    text = text.lower().replace(" ", "")
    table = {}
    final_table = ''
    for letter in alphabet:
        table[letter] = 0

    for letter in text:
        table[letter] += 1

    letters_in_order = sorted(table, key=table.get, reverse=True)

    for letter in letters_in_order:
        final_table = final_table + letter + ' '

    final_table += '\n'

    for letter in letters_in_order:
        final_table = final_table + str(table[letter]) + ' '

    print('\n', final_table)


def ind_co(text):
    text = text.lower().replace(" ", "")
    length = len(text)
    table = {}

    for letter in alphabet:
        table[letter] = 0

    for letter in text:
        table[letter] += 1

    answer = 0
    for letter in alphabet:
        frequency = table[letter]
        if frequency > 0:
            answer += frequency * (frequency - 1)
    answer /= length * (length - 1)

    return answer


def mut_ind_co(text1, text2):
    text1 = text1.lower().replace(" ", "")
    length1 = len(text1)
    table1 = {}

    text2 = text2.lower().replace(" ", "")
    length2 = len(text2)
    table2 = {}

    for letter in alphabet:
        table1[letter] = 0
        table2[letter] = 0

    for letter in text1:
        table1[letter] += 1

    for letter in text1:
        table2[letter] += 1

    answer = 0
    for letter in alphabet:
        answer += table1[letter] * table2[letter]
    answer /= length1 * length2

    return answer


def pollard_discrete_log(g, h, p):
    # solving for k in g^n = h (mod p)
    x = y = 1
    a = b = c = d = 0
    for i in range(0, p):
        x, a, b = pollard_f(x, g, h, p, a, b)
        y, c, d = pollard_f(y, g, h, p, c, d)
        y, c, d = pollard_f(y, g, h, p, c, d)

        if x == y:
            u = (a - c) % (p - 1)
            v = (d - b) % (p - 1)

            if v == 0:
                return u

            gcd = fractions.gcd(v, p - 1)
            if d == 1:
                return (u * inv(v, p-1)) % (p-1)
            else:
                s = extended_euclidean(v, p-1) % (p-1)
                w = (s * u) % (p-1)

                e = int(w/gcd)
                f = int((p-1)/gcd)

                for k in range(0, gcd):
                    n = e + k*f
                    if g ** n % p == h:
                        return n


def pollard_f(x, g, h, p, a, b):
    if 0 <= x < p/3:
        x = (g * x) % p
        a = (a + 1) % (p-1)
    elif p/3 <= x < 2*p/3:
        x = (x ** 2) % p
        a = (2 * a) % (p-1)
        b = (2 * b) % (p-1)
    elif 2*p/3 <= x < p:
        x = (h * x) % p
        b = (b + 1) % (p-1)
    return x, a, b


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


def extended_euclidean(a, b):
    # cite Wikipedia/Extended_Euclidean_algorithm
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a
    while r != 0:
        quotient = int(old_r / r)
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s