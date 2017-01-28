#!/usr/bin/env python3

"""

Reduce lambda expression

"""

from calculus import Variable, Abstraction, Application, β_reduction
from parser import tokenize, parse

def evaluate(term):
    if isinstance(term, Variable):
        return term
    elif isinstance(term, Abstraction):
        return Abstraction(term.variable, evaluate(term.term))
    elif isinstance(term, Application):
        if isinstance(term.term1, Abstraction):
            return β_reduction(term)
        else:
            return Application(evaluate(term.term1), evaluate(term.term2))

if __name__ == '__main__':
    from sys import stdin

    exp = parse(tokenize(stdin.read()))

    while True:
        exp1 = evaluate(exp)

        if str(exp) == str(exp1):
            break

        exp = exp1

    print(exp)
