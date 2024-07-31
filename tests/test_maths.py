import unittest
from decimal import InvalidOperation

import _set_source_path  # noqa # pyright: ignore

from source.maths import add, div, mnum, mul, sub, true_div


class TestMaths(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(mnum('1'), mnum('2')), ('3', '0'))
        self.assertEqual(add(mnum('1.0'), mnum('2')), ('3.0', '0.0'))
        self.assertEqual(add(mnum('0.1'), mnum('0.2')), ('0.3', '0.0'))
        self.assertEqual(add(mnum('5'), mnum('5')), ('10', '0'))
        self.assertEqual(add(mnum('6.5'), mnum('1.5')), ('8.0', '1.0'))
        self.assertEqual(add(mnum('6.5'), mnum('-1.5')), ('5.0', '0.0'))
        self.assertEqual(add(mnum('10'), mnum('10')), ('20', '00'))
        self.assertEqual(add(mnum('10'), mnum('-10')), ('00', '00'))
        self.assertEqual(add(mnum('-10'), mnum('-10')), ('-20', '00'))
        self.assertEqual(add(mnum('10'), mnum('-12')), ('-02', '00'))
        self.assertEqual(add(mnum('-50'), mnum('60')), ('10', '00'))
        self.assertEqual(add(mnum('-50'), mnum('-60')), ('-110', '00'))

    def test_sub(self) -> None:
        self.assertEqual(sub(mnum('1'), mnum('2')), ('-1', '0'))
        self.assertEqual(sub(mnum('1.0'), mnum('2')), ('-1.0', '0.0'))
        self.assertEqual(sub(mnum('0.1'), mnum('0.2')), ('-0.1', '0.0'))
        self.assertEqual(sub(mnum('5'), mnum('5')), ('0', '0'))
        self.assertEqual(sub(mnum('6.5'), mnum('1.5')), ('5.0', '0.0'))
        self.assertEqual(sub(mnum('6.5'), mnum('-1.5')), ('8.0', '1.0'))
        self.assertEqual(sub(mnum('10'), mnum('10')), ('00', '00'))
        self.assertEqual(sub(mnum('10'), mnum('-10')), ('20', '00'))
        self.assertEqual(sub(mnum('-10'), mnum('-10')), ('00', '00'))
        self.assertEqual(sub(mnum('10'), mnum('12')), ('-02', '00'))
        self.assertEqual(sub(mnum('-50'), mnum('-40')), ('-10', '00'))
        self.assertEqual(sub(mnum('-50'), mnum('-60')), ('10', '00'))

    # fmt: off
    def test_mul(self) -> None:
        self.assertEqual(mul(mnum('0'), mnum('0')), ('0', ['0'], ['0']))
        self.assertEqual(mul(mnum('1'), mnum('0')), ('0', ['0'], ['0']))
        self.assertEqual(mul(mnum('1'), mnum('1')), ('1', ['1'], ['0']))
        self.assertEqual(mul(mnum('1'), mnum('2')), ('2', ['2'], ['0']))
        self.assertEqual(mul(mnum('1.0'), mnum('2')), ('2.0', ['20'], ['0.0']))
        self.assertEqual(mul(mnum('0.1'), mnum('0.2')), ('0.02', ['02', '000'], ['0.0', '0.0']))
        self.assertEqual(mul(mnum('5'), mnum('5')), ('25', ['25'], ['0']))
        self.assertEqual(mul(mnum('6.5'), mnum('1.5')), ('9.75', ['325', '650'], ['2.0', '0.0']))
        self.assertEqual(mul(mnum('6.5'), mnum('-1.5')), ('-9.75', ['325', '650'], ['2.0', '0.0']))
        self.assertEqual(mul(mnum('-6.5'), mnum('-1.5')), ('9.75', ['325', '650'], ['2.0', '0.0']))
        self.assertEqual(mul(mnum('65.5'), mnum('2')), ('131.0', ['1310'], ['11.0']))
        self.assertEqual(mul(mnum('65.0'), mnum('2')), ('130.0', ['1300'], ['10.0']))
        self.assertEqual(mul(mnum('65.0'), mnum('2.0')), ('130.00', ['000', '13000'], ['00.0', '10.0']))

    def test_div(self) -> None:
        with self.assertRaises(InvalidOperation):
            _ = div(mnum('0'), mnum('0'))
        with self.assertRaises(ZeroDivisionError):
            _ = div(mnum('1'), mnum('0'))
            _ = div(mnum('12'), mnum('0'))

        self.assertEqual(div(mnum('0'), mnum('1')), ('0', [0], [0], [0]))
        self.assertEqual(div(mnum('0'), mnum('-1')), ('-0', [0], [0], [0]))
        self.assertEqual(div(mnum('1'), mnum('1')), ('1', [1], [1], [0]))
        self.assertEqual(div(mnum('1'), mnum('2')), ('0', [1], [0], [1]))
        self.assertEqual(div(mnum('1'), mnum('-2')), ('-0', [1], [0], [1]))
        self.assertEqual(div(mnum('-1'), mnum('2')), ('-0', [-1], [-0], [-1]))
        self.assertEqual(div(mnum('-1'), mnum('-2')), ('0', [-1], [-0], [-1]))
        self.assertEqual(div(mnum('101'), mnum('2')), ('50', [10], [10], [0]))
        self.assertEqual(div(mnum('1001'), mnum('2')), ('500', [10], [10], [0]))
        self.assertEqual(div(mnum('22'), mnum('7')), ('3', [22], [21], [1]))
        self.assertEqual(div(mnum('-22'), mnum('7')), ('-3', [-22], [-21], [-1]))
        self.assertEqual(div(mnum('22'), mnum('-7')), ('-3', [22], [21], [1]))
        self.assertEqual(div(mnum('-22'), mnum('-7')), ('3', [-22], [-21], [-1]))
        self.assertEqual(div(mnum("365"), mnum("-2")), ('-182', [3, 16, 5], [2, 16, 4], [1, 0, 1]))

    def test_true_div(self) -> None:
        with self.assertRaises(InvalidOperation):
            _ = div(mnum('0'), mnum('0'))
        with self.assertRaises(ZeroDivisionError):
            _ = div(mnum('1'), mnum('0'))
            _ = div(mnum('12'), mnum('0'))

        precision = 30  # number of decimal places.

        self.assertEqual(true_div(mnum('0'), mnum('1'), precision), ('0', [0], [0], [0]))
        self.assertEqual(true_div(mnum('0'), mnum('-1'), precision), ('-0', [0], [0], [0]))
        self.assertEqual(true_div(mnum('1'), mnum('1'), precision), ('1', [1], [1], [0]))
        self.assertEqual(true_div(mnum('1'), mnum('2'), precision), ('0.5', [10], [10], [0]))
        self.assertEqual(true_div(mnum('1'), mnum('-2'), precision), ('-0.5', [10], [10], [0]))
        self.assertEqual(true_div(mnum('-1'), mnum('2'), precision), ('-0.5', [-10], [-10], [0]))
        self.assertEqual(true_div(mnum('-1'), mnum('-2'), precision), ('0.5', [-10], [-10], [0]))
        self.assertEqual(true_div(mnum('101'), mnum('2'), precision), ('50.5', [10, 10], [10, 10], [0, 0]))
        self.assertEqual(true_div(mnum('1001'), mnum('2'), precision), ('500.5', [10, 10], [10, 10], [0, 0]))

        self.assertEqual(true_div(
            mnum("365"), mnum("-2"), 15),
            ('-182.5', [3, 16, 5, 10], [2, 16, 4, 10], [1, 0, 1, 0])
        )
        self.assertEqual(true_div(
            mnum('22'), mnum('7'), 15),
            ('3.142857142857142',
             [22, 10, 30, 20, 60, 40, 50, 10, 30, 20, 60, 40, 50, 10, 30, 20],
             [21, 7, 28, 14, 56, 35, 49, 7, 28, 14, 56, 35, 49, 7, 28, 14],
             [1, 3, 2, 6, 4, 5, 1, 3, 2, 6, 4, 5, 1, 3, 2, 6])
        )
        self.assertEqual(true_div(
            mnum('-22'), mnum('7'), 15),
            ('-3.142857142857142',
             [-22, -10, -30, -20, -60, -40, -50, -10, -30, -20, -60, -40, -50, -10, -30, -20],
             [-21, -7, -28, -14, -56, -35, -49, -7, -28, -14, -56, -35, -49, -7, -28, -14],
             [-1, -3, -2, -6, -4, -5, -1, -3, -2, -6, -4, -5, -1, -3, -2, -6])
        )
        self.assertEqual(true_div(
            mnum('22'), mnum('-7'), 15),
            ('-3.142857142857142',
             [22, 10, 30, 20, 60, 40, 50, 10, 30, 20, 60, 40, 50, 10, 30, 20],
             [21, 7, 28, 14, 56, 35, 49, 7, 28, 14, 56, 35, 49, 7, 28, 14],
             [1, 3, 2, 6, 4, 5, 1, 3, 2, 6, 4, 5, 1, 3, 2, 6])
        )
        self.assertEqual(true_div(
            mnum('-22'), mnum('-7'), 15),
            ('3.142857142857142',
             [-22, -10, -30, -20, -60, -40, -50, -10, -30, -20, -60, -40, -50, -10, -30, -20],
             [-21, -7, -28, -14, -56, -35, -49, -7, -28, -14, -56, -35, -49, -7, -28, -14],
             [-1, -3, -2, -6, -4, -5, -1, -3, -2, -6, -4, -5, -1, -3, -2, -6])
        )
    # fmt: on


if __name__ == '__main__':
    unittest.main()
