from discord.ext import commands
from application.prime_solver import exhaustive_solver, random_solver, common


class SacredGeometry(commands.Cog):
    primes = (
        (3, 5, 7),
        (11, 13, 17),
        (19, 23, 29),
        (31, 37, 41),
        (43, 47, 53),
        (59, 61, 67),
        (71, 73, 79),
        (83, 89, 97),
        (101, 103, 107),
    )

    level_min = 1
    level_max = 9
    roll_min = 1
    roll_max = 6
    spell_level_offset = 1

    exhaustive_warning_threshold = 8

    def __init__(self, bot, exhaustive_limit=8):
        self.bot = bot
        self.exhaustive_limit = exhaustive_limit

    @commands.command()
    async def solve(self, context, spell_level: int, *rolls: int):
        if not self._valid_spell_level(spell_level):
            invalid_level_message = (
                f"Spell level must be between {SacredGeometry.level_min} "
                f"and {SacredGeometry.level_max}."
            )
            await context.send(self._wrap_in_markdown(invalid_level_message))
        elif not self._valid_rolls(rolls):
            invalid_rolls_message = (
                f"Rolls must be between {SacredGeometry.roll_min} and {SacredGeometry.roll_max}."
            )
            await context.send(self._wrap_in_markdown(invalid_rolls_message))
        else:
            target_primes = self._get_target_primes(spell_level)
            number_of_rolls = len(rolls)

            if number_of_rolls <= self.exhaustive_limit:
                await context.send(self._wrap_in_markdown("Solving exhaustively..."))
                result = exhaustive_solver.solve(rolls, target_primes)
            else:
                await context.send(self._wrap_in_markdown("Solving randomly..."))
                result = random_solver.solve(rolls, target_primes)

            if result:
                (expression, total) = result
                expression_string = common.expression_to_string(expression)
                total = int(total)
                await context.send(self._wrap_in_markdown(f"{expression_string} = {total}"))
            else:
                await context.send(self._wrap_in_markdown("No solution was found."))

    @commands.command()
    async def list_primes(self, context):
        """Sends back a table of spell levels and corresponding prime values."""
        table = self._format_primes_to_table()
        await context.send(self._wrap_in_markdown(table))

    @commands.command()
    async def set_exhaustive_limit(self, context, limit: int):
        warning_message = (
            f"Warning: values greater than {SacredGeometry.exhaustive_warning_threshold} "
            f"may incur long solving times."
        )

        if limit > SacredGeometry.exhaustive_warning_threshold:
            await context.send(self._wrap_in_markdown(warning_message))

        await context.send(self._wrap_in_markdown(f"Exhaustive limit set to: {limit}"))
        self.exhaustive_limit = limit

    @property
    def exhaustive_limit(self):
        return self._exhaustive_limit

    @exhaustive_limit.setter
    def exhaustive_limit(self, exhaustive_limit):
        self._exhaustive_limit = exhaustive_limit

    def _valid_spell_level(self, level):
        if (
            level >= SacredGeometry.level_min
            and level <= SacredGeometry.level_max
        ):
            return True
        else:
            return False

    def _valid_rolls(self, rolls):
        for roll in rolls:
            if roll < SacredGeometry.roll_min or roll > SacredGeometry.roll_max:
                return False

        return True

    def _get_target_primes(self, spell_level):
        """Converts a spell level to a list index, with the minimum level being 1."""
        target_primes = SacredGeometry.primes[spell_level - SacredGeometry.spell_level_offset]
        return target_primes

    def _wrap_in_markdown(self, string):
        return f"```python\n{string}\n```"

    def _format_primes_to_table(self):
        table = "+-------+---------------+\n"
        table += "| Level |    Primes     |\n"
        table += "+-------+---------------+\n"

        for level, target_primes_tuple in enumerate(SacredGeometry.primes):
            level += SacredGeometry.spell_level_offset
            target_primes_string = ", ".join(map(str, target_primes_tuple))

            if level == SacredGeometry.level_min:
                table += f"|   {level}   | {target_primes_string}       |\n"
            elif level == SacredGeometry.level_max:
                table += f"|   {level}   | {target_primes_string} |\n"
            else:
                table += f"|   {level}   | {target_primes_string}    |\n"
            table += "+-------+---------------+\n"

        return table
