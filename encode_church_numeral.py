#!/usr/bin/env python3

"""

Encode Church numeral

"""

from calculus import Variable, Abstraction, Application

def encode_church_numeral(n):
    term = Variable("x")
    for _ in range(n):
        term = Application(Variable("f"), term)

    return Abstraction(Variable("f"), Abstraction(Variable("x"), term))

if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1])
        print(encode_church_numeral(n))
    except (IndexError, ValueError):
        print("Usage: python3 %s n" % sys.argv[0])
