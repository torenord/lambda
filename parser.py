#!/usr/bin/env python3

"""

Parse lambda expression

"""

from collections import deque
from calculus import Variable, Abstraction, Application

def tokenize(inp):
    inp = inp.replace("\n", " ")

    inp = inp.replace("(", " ( ").replace(")", " ) ")
    inp = inp.replace(".", "")

    while True:
        inp1 = inp.replace("  ", " ")
        if inp == inp1:
            break
        inp = inp1

    inp = inp.strip()

    tokens = deque(inp.split(" "))

    return tokens

def parse(tokens):
    def parse_inner(tokens):
        if len(tokens) == 0:
            raise Exception("parse error")

        token = tokens.popleft()

        if token != "(":
            return Variable(token)
        else:
            if tokens[0] == "λ":
                tokens.popleft()
                exp = Abstraction(parse_inner(tokens), parse_inner(tokens))
            else:
                exp = Application(parse_inner(tokens), parse_inner(tokens))

            tokens.popleft()
            return exp

    exp = parse_inner(tokens)

    if len(tokens) > 0:
        raise Exception("parse error")

    return exp
