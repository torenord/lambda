"""

Lambda calculus

"""

def f():
    fresh_variable_counter = 0

    def g():
        nonlocal fresh_variable_counter
        fresh_variable_counter += 1
        return Variable("v" + str(fresh_variable_counter))

    return g

fresh_variable = f()

class Term: pass

class Variable(Term):
    def __init__(self, variable):
        self.variable = variable

    def __eq__(self, other):
        return self.variable == other.variable

    def __hash__(self):
        return hash(self.variable)

    def __repr__(self):
        return self.variable

class Abstraction(Term):
    def __init__(self, variable, term):
        if not isinstance(variable, Variable):
            raise ValueError(str(variable) + " is not an instance of Variable")
        if not isinstance(term, Term):
            raise ValueError(str(term) + " is not an instance of Term")

        self.variable = variable
        self.term = term

    def __repr__(self):
        return "(λ %s . %s)" % (self.variable, self.term)

class Application(Term):
    def __init__(self, term1, term2):
        if not isinstance(term1, Term):
            raise ValueError(str(term1) + " is not an instance of Term")
        if not isinstance(term2, Term):
            raise ValueError(str(term2) + " is not an instance of Term")

        self.term1 = term1
        self.term2 = term2

    def __repr__(self):
        return "(%s %s)" % (self.term1, self.term2)

def FV(term):
    if isinstance(term, Variable):
        return {term}
    elif isinstance(term, Abstraction):
        return FV(term.term) - {term.variable}
    elif isinstance(term, Application):
        return FV(term.term1) | FV(term.term2)
    else:
        raise ValueError(str(term) + " is not an instance of Term")

def BV(term):
    if isinstance(term, Variable):
        return set()
    elif isinstance(term, Abstraction):
        return BV(term.term) | {term.variable}
    elif isinstance(term, Application):
        return BV(term.term1) | BV(term.term2)
    else:
        raise ValueError(str(term) + " is not an instance of Term")

def substitution(term1, variable, term2):
    if not isinstance(term1, Term):
        raise ValueError(str(term1) + " is not an instance of Term")
    if not isinstance(variable, Variable):
        raise ValueError(str(term2) + " is not an instance of Variable")
    if not isinstance(term2, Term):
        raise ValueError(str(term2) + " is not an instance of Term")

    if isinstance(term1, Variable):
        if term1 == variable:
            return term2
        else:
            return term1
    elif isinstance(term1, Abstraction):
        if term1.variable == variable:
            return term1
        else:
            if term1.variable in FV(term2):
                return substitution(
                    α_conversion(term1, fresh_variable()),
                    variable,
                    term2
                )
            else:
                return Abstraction(
                    term1.variable,
                    substitution(term1.term, variable, term2)
                )
    elif isinstance(term1, Application):
        return Application(
            substitution(term1.term1, variable, term2),
            substitution(term1.term2, variable, term2)
        )

def α_conversion(term, variable):
    if not isinstance(term, Abstraction):
        raise ValueError(str(term) + " is not an instance of Abstraction")
    if not isinstance(variable, Variable):
        raise ValueError(str(variable) + " is not an instance of Variable")

    if variable in FV(term.term):
        raise Exception(variable + " must be free in ")

    return Abstraction(
        variable,
        substitution(term.term, term.variable, variable)
    )

def β_reduction(term):
    return substitution(term.term1.term, term.term1.variable, term.term2)
