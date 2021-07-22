"""A module designed to randomly resolve a set of values into a set of target values."""


import random

from application.prime_solver import common


_DEFAULT_ITERATIONS = 1000000


def solve(values, target_values, iterations=_DEFAULT_ITERATIONS):
    for i in range(iterations):
        values_list = list(values)
        random.shuffle(values_list)
        values = tuple(values_list)

        total = values[0]
        expression = ()

        for value in values[1:]:
            operation = random.choice(list(common.OPERATIONS.values()))

            total = common.perform_operation(total, operation, value)

            if total is None:
                break

            if not expression:
                expression = (total)
            else:
                expression = (expression, operation, value)

        if total in target_values:
            return (expression, total)
