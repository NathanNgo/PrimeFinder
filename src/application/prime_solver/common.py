"""A module containing common variables and functions to all solvers"""


ADD_KEY = "Add"
SUB_KEY = "Sub"
MUL_KEY = "Mul"
DIV_KEY = "Div"
_ADD = '+'
_SUB = '-'
_MUL = '*'
_DIV = '/'
OPERATIONS = {
    ADD_KEY: _ADD,
    SUB_KEY: _SUB,
    MUL_KEY: _MUL,
    DIV_KEY: _DIV
}


def perform_operation(first, operation, second):
    if operation == _ADD:
        first += second
    elif operation == _SUB:
        first -= second
    elif operation == _MUL:
        first *= second
    elif operation == _DIV:
        try:
            first /= second
        except ZeroDivisionError:
            return None

    return first


def expression_to_string(expression):
    if not isinstance(expression[0], tuple):
        expression_string = ' '.join(map(str, expression))
    else:
        expression_string = ' '.join(
            map(str, [expression_to_string(expression[0])] + list(expression[1:]))
        )

    return f"({expression_string})"
