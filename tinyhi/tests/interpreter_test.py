import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from tinyhi.execution import run

INTERPRETER_TESTS = {
    'fact': [r"""
      BEGIN TEST
        BEGIN DOIT(N)
            BEGIN FACT(N)
                IF N = 0
                    FACT <- 1
                ELSE
                    FACT <- N * FACT(N - 1)
                END
            END
            DOIT <- FACT(2 * N)
        END
        DOIT(3)
      END
    """, '720'],
    'bagl': [r"""
      BEGIN PROG
        A <- "ALGEBRA"
        A[5 1 3 2]
      END
    """, 'BAGL'],
    'gcf': [r"""
      BEGIN MAIN
          BEGIN MOD(A, B)
              MOD <- A-B*(A/B)
          END
          BEGIN GCF(XD, YD)
              X <- XD
              Y <- YD
              IF X < Y
                  T <- X
                  X <- Y
                  Y <- T
                  T <-
              END
              R <- Y
              WHILE R > 0
                  R <- MOD(X, Y)
                  X <- Y
                  Y <- R
              END
              GCF <- X
          END
          GCF(2*3*5*5*7,2*2*3*5)
      END
    """, '30'],
    'no_args': [r"""
      BEGIN PROG
        BEGIN NOARG
          1
          NOARG <- -1
        END
        TEMP <- NOARG()
      END
    """, '1'],
    'inner_call': [r"""
      BEGIN PROG
        BEGIN FUNC(X)
          BEGIN CALL(Y)
            0
            CALL <- "CALL"
          END
          TEMP <- CALL(0)
          1
          FUNC <- "FUNC"
        END
        TEMP <- FUNC(0)
        2
      END
    """, '0\n1\n2'],
    'no_inner_call': [r"""
      BEGIN PROG
        BEGIN FUNC(X)
          BEGIN NEVER(Y)
            0
            NEVER <- "NEVER"
          END
          1
          FUNC <- "FUNC"
        END
        TEMP <- FUNC(0)
        2
      END
    """, '1\n2'],
    'concat': [r"""
      BEGIN MAIN
        A <- 1 2
        A <- A 3 4
        A
      END
    """, '1 2 3 4'],
    'vecsum': [r"""
      BEGIN MAIN
        1 2 3 + 4 5 6
      END
    """, '5 7 9'],
    'strcat_0': [r"""
      BEGIN MAIN
        "AB" "CD"
      END
    """, 'ABCD'],
    'strcat_1': [r"""
      BEGIN MAIN
        A <- "AB"
        B <- "CD"
        A B
      END
    """, 'ABCD'],
    'bcast': [r"""
      BEGIN MAIN
        1 + 4 5 6
      END
    """, '5 6 7'],
    'length': [r"""
      BEGIN MAIN
        #5 73 -1
      END
    """, '3']
}


class TestInterpreter(unittest.TestCase):
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
    for name, (source, expected) in INTERPRETER_TESTS.items():
        setattr(TestInterpreter, 'test_{0}'.format(
            name), _make_test(source, expected))


add_interpreter_tests()

if __name__ == '__main__':
    unittest.main(exit=False)
