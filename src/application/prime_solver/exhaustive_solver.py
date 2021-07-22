"""A module designed to exhaustively resolve a set of values into a set of target values."""


from application.prime_solver import common


def solve(values, target_values):
    for index, initial_total in enumerate(values):
        initial_values = values[:index] + values[index + 1:]
        initial_expression = (initial_total)

        result = _recursive_finder(initial_values, initial_expression, initial_total, target_values)

        if result:
            return result


def _recursive_finder(values, expression, total, target_values):
    for operation in common.OPERATIONS.values():
        for index, value in enumerate(values):
            new_expression = (expression, operation, value)
            new_total = common.perform_operation(total, operation, value)
            remaining_values = values[:index] + values[index + 1:]

            if new_total is None:
                continue

            if remaining_values:
                result = _recursive_finder(
                    remaining_values, new_expression, new_total, target_values
                )

                if result:
                    return result

            elif not remaining_values and new_total in target_values:
                return (new_expression, new_total)
