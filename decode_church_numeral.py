#!/usr/bin/env python3

"""

Decode Church numeral

"""

from calculus import Abstraction, Application
from parser import tokenize, parse

def decode_church_numeral(exp):
    if not (isinstance(exp, Abstraction) and isinstance(exp.term, Abstraction)):
        raise ValueError("not Church numeral")

    a, b = exp.variable, exp.term.variable
    exp = exp.term.term
    counter = 0

    while isinstance(exp, Application) and exp.term1 == a:
        exp = exp.term2
        counter += 1

    if exp == b:
        return counter
    else:
        raise ValueError("not Church numeral")

if __name__ == '__main__':
    from sys import stdin
    print(decode_church_numeral(parse(tokenize(stdin.read()))))
