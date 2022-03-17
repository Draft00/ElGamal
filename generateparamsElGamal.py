
from sympy import nextprime


def generate_p(length):

    return nextprime(getrandbits(length))


from random import getrandbits


def generate_a(p, length):

    a = getrandbits(length)
    # phi_p = phi(p) - euler function
    phi_p = p - 1

    # a - Primitive root modulo p (a ^ phi(p) (mod p) = 1)
    while (pow(a, phi_p, p) != 1):
        a = getrandbits(length)

    return a


from random import randint
from sympy import gcd


def generate_x(p, length):

    x = randint(1, p)

    # x - случайное число из интервала (1, p), взаимно простое с p-1
    while (gcd(x, p - 1) != 1):
        x = randint(1, p)

    return x


# x = 0x2c056e6a6c8c307b4426303ff5b1d6c42d146fe6be6e568a7c4de2f95e072a20

from sys import argv


def generate_parameters(length = 512):

    try:
        length = int(argv[1])
    except:
        length = 512

    p = generate_p(length)
    a = generate_a(p, length)
    x = generate_x(p, length)

    b = pow(a, x, p)

    print('length_p =', length)
    print('p =', p)
    print('a =', a)
    # b = a^x (mod p)
    print('b =', b)
    print('')
    print('x =', x)


if __name__ == '__main__':
    generate_parameters()

