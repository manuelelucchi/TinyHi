from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import unittest
from tinyhi.parsing import Parse
from tinyhi.execution import run

PARSER_INTEGRATIVE_TESTS = {
    'interrupted': r"""
        BEGIN MAIN
            IF
        END
        """
}

INTERPRETER_INTERGATIVE_TESTS = {
    'vector_creation_1': [r"""
        BEGIN MAIN
            (1 2) 3
        END
        """, ''],
    'vector_creation_2': [r"""
        BEGIN MAIN
            1 (2 3)
        END
        """, ''],
    'vector_creation_3': [r"""
        BEGIN MAIN
            V <- 1 2
            V 3
        END
        """, ''],
    'vector_creation_4': [r"""
        BEGIN MAIN
            V <- 2 3
            1 V
        END
        """, ''],
    "broadcasting_1": [r"""
        BEGIN MAIN
            ~ 2 3 + 1
        END
        """, ''],
    "broadcasting_2": [r"""
        BEGIN MAIN
            1 - 2 3
        END
        """, ''],
    "broadcasting_3": [r"""
        BEGIN MAIN
            0 / (1 2)
        END
        """, ''],
    "illegal_call": [r"""
        BEGIN TEST
            BEGIN ABACO
                DOIT(3)
            END
            BEGIN DOIT(N)
                N
            END
            ABACO()
        END
    """, ''],
    "global_var_0": [r"""
        BEGIN MAIN
            1
            .C <- 1
            .C
        END
        """, ''],
    "global_var_1": [r"""
        BEGIN MAIN
            X <- 0
            WHILE X < 10
                X <- X + 1
                .C <- X
            END
            .C
        END
        """, ''],
    "simple_loop_1": [r"""
        BEGIN MAIN
            X <- 1
            WHILE X < 10
                X <- X + 2
            END
            X
        END
        """, ''],
    "very_long_loop": [r"""
        BEGIN MAIN
            X <- 1
            WHILE X < 3000000
                X <- X + 1
            END
            X
        END
        """, ''],
    "variable_not_declared": [r"""
        BEGIN MAIN
            IF X < 10
                1
            END
        END
        """, ''],
    "different_size_sum": [r"""
        BEGIN MAIN
            TWO <- 1 1
            THREE <- 1 1 1
            TWO + THREE
        END
        """, '']
}


class TestParserIntegrative(unittest.TestCase):
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
    for name, source in PARSER_INTEGRATIVE_TESTS.items():
        setattr(TestParserIntegrative, 'test_{0}'.format(
            name), _make_test(source))


class TestInterpreterIntegrative(unittest.TestCase):
    pass


def add_interpreter_tests():
    def _make_test(source, expected):
        def _test(self):
            actual = StringIO()
            try:
                with redirect_stdout(actual):
                    run(source)
            except Exception as e:
                self.fail('Exception: {}'.format(e))
            self.assertEqual(expected, actual.getvalue().strip())
        return _test
    for name, (source, expected) in INTERPRETER_INTERGATIVE_TESTS.items():
        setattr(TestInterpreterIntegrative, 'test_{0}'.format(
            name), _make_test(source, expected))


add_parser_tests()
add_interpreter_tests()

if __name__ == '__main__':
    unittest.main(exit=False)
