import itertools

def primes():
    p = 1
    fact = 1
    while True:
        fact *= p
        p += 1
        if (fact + 1) % p == 0:
            yield p

print(list(itertools.takewhile(lambda x : x <= 31, primes())))