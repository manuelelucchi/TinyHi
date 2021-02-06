from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import unittest
from tinyhi.parsing import Parse

PARSER_TESTS = {
    'block_named': r"""
      BEGIN PROG
        1
      END
    """,
    'block_args1': r"""
      BEGIN MAIN
        BEGIN ARG(ONE)
          1
        END
        1
      END
    """,
    'block_args2': r"""
      BEGIN MAIN
        BEGIN ARG(ONE, TWO)
          1
        END
        1
      END
    """,
    'block_nested': r"""
      BEGIN OUTER
        BEGIN INNER
          1
        END
        1
      END
    """,
    'block_parallel': r"""
      BEGIN OUTER
        BEGIN ONE
          1
        END
        BEGIN TWO
          1
        END
        1
      END
    """,
    'assignement': r"""
      BEGIN PROG
        X <- 1
      END
    """,
    'empty_assignement': r"""
      BEGIN PROG
        X <-
      END
    """,
    'exprstm': r"""
      BEGIN PROG
        1 + 2
      END
    """,
    'if': r"""
      BEGIN PROG
        IF X < 1
          1
        END
      END
    """,
    'ifelse': r"""
      BEGIN PROG
        IF X < 1
          1
        ELSE
          2
        END
      END
    """,
    'while': r"""
      BEGIN PROG
        WHILE X < 1
          1
        END
      END
    """,
    'until': r"""
      BEGIN PROG
        UNTIL X < 1
          1
        END
      END
    """,
    'atoms': r"""
      BEGIN PROG
        X <- 1
        X <- "TEST"
        X <- A
        X <- .A
        X <- F(1)
        X <- F("ONE")
        X <- F(1, 2)
        X <- F("ONE", "TWO")
      END
    """,
    'unary': r"""
      BEGIN PROG
        X <- -1
        X <- ~ 1
        X <- ~1
        X <- # 1
        X <- #1
      END
    """,
    'binops': r"""
      BEGIN PROG
        X <- 1 + 2
        X <- 1 - 2
        X <- 1 / 2
        X <- 1 * 2
      END
    """,
    'conds': r"""
      BEGIN PROG
        IF X < 1
          1
        END
        IF X <= 1
          1
        END
        IF X = 1
          1
        END
        IF X <> 1
          1
        END
        IF X >= 1
          1
        END
        IF X > 1
          1
        END
      END
    """,
    'list': r"""
      BEGIN PROG
        X <- 1 2 3
        X <- "ONE" "TWO" "THREE"
        X <- 1 A F(1)
        X <- "ONE" A F("ONE")
      END
    """,
    'expr_list': r"""
      BEGIN PROG
        X <- 1 2 + 3 4
        X <- 1 + # 2 3
        X <- 2 + ~ 1
      END
    """,
    'expr_func': r"""
      BEGIN PROG
        X <- F(1 2)
        X <- 1 F(1) G (2)
      END
    """,
    'expr_prec': r"""
      BEGIN PROG
        X <- 1 + 2 * 3
        X <- 1 ~ 2 * 3
        X <- 1 # 2 * 3
      END
    """,
    'block_args0_call': r"""
      BEGIN PROG
        BEGIN ZERO
        1
        END
        ZERO()
      END
    """,
    'empty_line_0': r"""
      BEGIN PROG
        1
        2
      END
    """,
    'empty_line_1': r"""
      BEGIN PROG
        1
        2
      END
    """,
    'empty_line_2': r"""
      BEGIN PROG
        1
        2
      END
    """,
    'empty_line_if_0': r"""
      BEGIN MAIN
        IF X < 1
            1
        END
      END
    """,
    'empty_line_if_1': r"""
      BEGIN MAIN
        IF X < 1
            1
        END
      END
    """,
    'empty_line_while_0': r"""
      BEGIN MAIN
        WHILE X < 1
            1
        END
      END
    """,
    'empty_line_while_1': r"""
      BEGIN MAIN
        WHILE X < 1
            1
        END
      END
    """,
    'empty_line_until_0': r"""
      BEGIN MAIN
        UNTIL X < 1
            1
        END
      END
    """,
    'empty_line_until_1': r"""
      BEGIN MAIN
        UNTIL X < 1
            1
        END
      END
    """
}


class TestParser(unittest.TestCase):
    pass


def add_parser_tests():
    def _make_test(source):
        def _test(self):
            try:
                with redirect_stdout(StringIO()):
                    Parse(source)
            except Exception as e:
                self.fail('Exception: {}'.format(e))
        return _test
    for name, source in PARSER_TESTS.items():
        setattr(TestParser, 'test_{0}'.format(name), _make_test(source))


add_parser_tests()
if __name__ == '__main__':
    unittest.main(exit=False)
