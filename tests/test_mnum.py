import unittest

import _set_source_path  # noqa # pyright: ignore

from source.mnum import mnum


class TestMnum(unittest.TestCase):
    def test_sign(self) -> None:
        self.assertEqual(mnum(0) == 0, True)
        self.assertEqual(- mnum(1) < 0, True)
        self.assertEqual(abs(mnum(-5)) > 0, True)

    def test_compare(self) -> None:
        self.assertEqual(bool(mnum(0)), False)
        self.assertEqual(bool(mnum(1)), True)
        self.assertEqual(bool(mnum(-1)), True)

        self.assertEqual(mnum(1) == 1, True)
        self.assertEqual(mnum(1) != 1, False)
        self.assertEqual(mnum(1) < 2, True)
        self.assertEqual(mnum(1) <= 2, True)
        self.assertEqual(mnum(1) > 0, True)
        self.assertEqual(mnum(1) >= 0, True)
        self.assertEqual(mnum(1) == 0, False)
        self.assertEqual(mnum(1) != 0, True)
        self.assertEqual(mnum(1) < 0, False)
        self.assertEqual(mnum(1) <= 0, False)

    def test_add(self) -> None:
        self.assertEqual(mnum(1) + 1, 2)
        self.assertEqual(mnum(1) + 0, 1)
        self.assertEqual(mnum(1) + (-1), 0)
        self.assertEqual(mnum(1) + mnum(1), 2)
        self.assertEqual(mnum(1) + mnum(0), 1)
        self.assertEqual(mnum(1) + mnum(-1), 0)
        self.assertEqual(mnum(1) + mnum(0.5), 1.5)
        self.assertEqual(mnum(1) + mnum(-0.5), 0.5)
        self.assertEqual(mnum(1) + mnum(0.25), 1.25)
        self.assertEqual(mnum(1) + mnum(-0.25), 0.75)
        self.assertEqual(mnum(1) + mnum(0.125), 1.125)
        self.assertEqual(mnum(1) + mnum(-0.125), 0.875)
        self.assertEqual(mnum(1) + mnum(0.0625), 1.0625)

        self.assertEqual(mnum('1') + mnum('0.2'), mnum('1.2'))
        self.assertEqual(mnum('0.1') + mnum('0.2'), mnum('0.3'))
        self.assertEqual(mnum('-0.1') + mnum('0.2'), mnum('0.1'))
        self.assertEqual(mnum('0.1') + mnum('-0.2'), mnum('-0.1'))
        self.assertEqual(mnum('25.65') + mnum('-0.65'), mnum('25.0'))
        self.assertEqual(mnum('-25.65') + mnum('0.65'), mnum('-25.0'))
        self.assertEqual(mnum('2226.35') + mnum('26.55'), mnum('2252.90'))

    def test_subtract(self) -> None:
        self.assertEqual(mnum(1) - 1, 0)
        self.assertEqual(mnum(1) - 0, 1)
        self.assertEqual(mnum(1) - (-1), 2)
        self.assertEqual(mnum(1) - mnum(1), 0)
        self.assertEqual(mnum(1) - mnum(0), 1)
        self.assertEqual(mnum(1) - mnum(-1), 2)
        self.assertEqual(mnum(1) - mnum(0.5), 0.5)
        self.assertEqual(mnum(1) - mnum(-0.5), 1.5)
        self.assertEqual(mnum(1) - mnum(0.25), 0.75)
        self.assertEqual(mnum(1) - mnum(-0.25), 1.25)
        self.assertEqual(mnum(1) - mnum(0.125), 0.875)
        self.assertEqual(mnum(1) - mnum(-0.125), 1.125)
        self.assertEqual(mnum(1) - mnum(0.0625), 0.9375)

        self.assertEqual(mnum('1') - mnum('0.2'), mnum('0.8'))
        self.assertEqual(mnum('0.1') - mnum('0.2'), mnum('-0.1'))
        self.assertEqual(mnum('-0.1') - mnum('0.2'), mnum('-0.3'))
        self.assertEqual(mnum('0.1') - mnum('-0.2'), mnum('0.3'))
        self.assertEqual(mnum('25.65') - mnum('-0.65'), mnum('26.3'))
        self.assertEqual(mnum('-25.65') - mnum('0.65'), mnum('-26.3'))
        self.assertEqual(mnum('2226.35') - mnum('26.55'), mnum('2199.80'))

    def test_multiply(self) -> None:
        self.assertEqual(mnum(1) * 1, 1)
        self.assertEqual(mnum(1) * 0, 0)
        self.assertEqual(mnum(1) * (-1), -1)
        self.assertEqual(mnum(1) * mnum(1), 1)
        self.assertEqual(mnum(1) * mnum(0), 0)
        self.assertEqual(mnum(1) * mnum(-1), -1)
        self.assertEqual(mnum(1) * mnum(0.5), 0.5)
        self.assertEqual(mnum(1) * mnum(-0.5), -0.5)
        self.assertEqual(mnum(1) * mnum(0.25), 0.25)
        self.assertEqual(mnum(1) * mnum(-0.25), -0.25)
        self.assertEqual(mnum(1) * mnum(0.125), 0.125)
        self.assertEqual(mnum(1) * mnum(-0.125), -0.125)
        self.assertEqual(mnum(1) * mnum(0.0625), 0.0625)

        self.assertEqual(mnum('1') * mnum('0.2'), mnum('0.2'))
        self.assertEqual(mnum('0.1') * mnum('0.2'), mnum('0.02'))
        self.assertEqual(mnum('-0.1') * mnum('0.2'), mnum('-0.02'))
        self.assertEqual(mnum('0.1') * mnum('-0.2'), mnum('-0.02'))
        self.assertEqual(mnum('25.65') * mnum('-0.65'), mnum('-16.6725'))
        self.assertEqual(mnum('-25.65') * mnum('0.65'), mnum('-16.6725'))
        self.assertEqual(mnum('2226.35') * mnum('26.55'), mnum('59109.5925'))

    def test_divide(self) -> None:
        # Test floor division
        self.assertEqual(mnum(0) // 1, 0)
        self.assertEqual(mnum(1) // 1, 1)
        self.assertEqual(mnum(1) // (-1), -1)
        self.assertEqual(mnum(1) // mnum(1), 1)
        self.assertEqual(mnum(0) // mnum(1), 0)
        self.assertEqual(mnum(1) // mnum(-1), -1)
        self.assertEqual(mnum(1) // mnum(0.5), 2)
        self.assertEqual(mnum(1) // mnum(-0.5), -2)
        self.assertEqual(mnum(1) // mnum(0.25), 4)
        self.assertEqual(mnum(1) // mnum(-0.25), -4)
        self.assertEqual(mnum(1) // mnum(0.125), 8)
        self.assertEqual(mnum(1) // mnum(-0.125), -8)
        self.assertEqual(mnum(1) // mnum(0.0625), 16)
        self.assertEqual(mnum(1) // mnum(-0.0625), -16)

        self.assertEqual(mnum('1') // mnum('0.2'), mnum('5'))
        self.assertEqual(mnum('0.1') // mnum('0.2'), mnum('0'))
        self.assertEqual(mnum('-0.1') // mnum('0.2'), mnum('-0'))
        self.assertEqual(mnum('0.1') // mnum('-0.2'), mnum('-0'))
        self.assertEqual(mnum('25.65') // mnum('-0.65'), mnum('-39'))
        self.assertEqual(mnum('-25.65') // mnum('0.65'), mnum('-39'))
        self.assertEqual(mnum('2226.35') // mnum('26.55'), mnum('83'))

        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            _ = mnum(10) // 0

        self.assertEqual(0 // mnum(12), 0)

        # Test true division
        self.assertEqual(mnum(0) / 1, 0)
        self.assertEqual(mnum(1) / 1, 1)
        self.assertEqual(mnum(1) / (-1), -1)
        self.assertEqual(mnum(1) / mnum(1), 1)
        self.assertEqual(mnum(0) / mnum(1), 0)
        self.assertEqual(mnum(1) / mnum(-1), -1)
        self.assertEqual(mnum(1) / mnum(0.5), 2)
        self.assertEqual(mnum(1) / mnum(-0.5), -2)
        self.assertEqual(mnum(1) / mnum(0.25), 4)
        self.assertEqual(mnum(1) / mnum(-0.25), -4)
        self.assertEqual(mnum(1) / mnum(0.125), 8)
        self.assertEqual(mnum(1) / mnum(-0.125), -8)
        self.assertEqual(mnum(1) / mnum(0.0625), 16)
        self.assertEqual(mnum(1) / mnum(-0.0625), -16)

        self.assertEqual(mnum('1') / mnum('0.2'), mnum('5'))
        self.assertEqual(mnum('0.1') / mnum('0.2'), mnum('0.5'))
        self.assertEqual(mnum('-0.1') / mnum('0.2'), mnum('-0.5'))
        self.assertEqual(mnum('0.1') / mnum('-0.2'), mnum('-0.5'))

        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            _ = mnum(10) / 0

        self.assertEqual(0 / mnum(12), 0)

    def test_indexing(self) -> None:
        self.assertEqual(mnum(0)[0], 0)
        self.assertEqual(mnum(1)[-1], 1)
        self.assertEqual(mnum(10)[0], 1)
        self.assertEqual(mnum(10)[1], 0)
        self.assertEqual(mnum(10)[-1], 0)

        self.assertEqual(mnum('0.1')[0], 0)
        self.assertEqual(mnum('1.0')[-1], 0)
        self.assertEqual(mnum('1.5')[1], 5)
        self.assertEqual(mnum('-1.5')[1], -5)
        self.assertEqual(mnum('-0.5')[-1], -5)
        self.assertEqual(mnum('-0.56')[2], -6)
        self.assertEqual(mnum('-1.56')[-1], -6)

        # Test out of bound index error
        with self.assertRaises(IndexError):
            _ = mnum(0)[1]
        with self.assertRaises(IndexError):
            _ = mnum(-1)[1]
        with self.assertRaises(IndexError):
            _ = mnum(5)[1]

        self.assertEqual(mnum('0').geti(0), 0)
        self.assertEqual(mnum('0.1').geti(0), 0)
        self.assertEqual(mnum('0.1').geti(-1), 0)
        self.assertEqual(mnum('1.0').geti(0), 1)
        self.assertEqual(mnum('1.5').geti(-1), 1)
        self.assertEqual(mnum('-1.5').geti(-1), -1)
        self.assertEqual(mnum('-1.56').geti(-1), -1)

        self.assertEqual(mnum('0.1').getf(0), 1)
        self.assertEqual(mnum('0.1').getf(-1), 1)
        self.assertEqual(mnum('1.0').getf(0), 0)
        self.assertEqual(mnum('1.5').getf(0), 5)
        self.assertEqual(mnum('-1.5').getf(0), -5)
        self.assertEqual(mnum('-1.56').getf(1), -6)

        self.assertEqual(mnum('0.1').geti(1), None)
        self.assertEqual(mnum('0.1').geti(-2), None)
        self.assertEqual(mnum('1.0').geti(1), None)
        self.assertEqual(mnum('1.5').geti(1), None)
        self.assertEqual(mnum('-1.5').geti(1), None)

        self.assertEqual(mnum('0.1').getf(1), None)
        self.assertEqual(mnum('0.1').getf(-2), None)
        self.assertEqual(mnum('1.0').getf(1), None)
        self.assertEqual(mnum('1.5').getf(1), None)
        self.assertEqual(mnum('-1.5').getf(1), None)
        self.assertEqual(mnum('-1.56').getf(2), None)

    def test_add_method(self) -> None:
        self.assertEqual(mnum(0).add(mnum(1)), 1)
        self.assertEqual(mnum(1).add(mnum(0)), 10)
        self.assertEqual(mnum(1).add(mnum(5)), 15)
        self.assertEqual(mnum(1).add(mnum(0.5)), 1.5)
        self.assertEqual(mnum(-1).add(mnum(0.5)), -1.5)
        self.assertEqual(mnum(0).add(mnum(-0.5)), -0.5)
        self.assertEqual(mnum(10).add(mnum(-0.5)), -10.5)
        self.assertEqual(mnum(0.5).add(mnum(5)), 5.5)
        self.assertEqual(mnum(-0.5).add(mnum(5)), -5.5)
        self.assertEqual(mnum('-0.5').add(mnum('0.5')), mnum('-0.55'))
        self.assertEqual(mnum('-0.5').add(mnum('0.56')), mnum('-0.556'))

    def test_join_method(self) -> None:
        def join(first: mnum, second: mnum) -> mnum:
            first.join(second)
            return first

        self.assertEqual(join(mnum(0), mnum(1)), 1)
        self.assertEqual(join(mnum(1), mnum(0)), 10)
        self.assertEqual(join(mnum(1), mnum(5)), 15)
        self.assertEqual(join(mnum(1), mnum(0.5)), 1.5)
        self.assertEqual(join(mnum(-1), mnum(0.5)), -1.5)
        self.assertEqual(join(mnum(0), mnum(-0.5)), -0.5)
        self.assertEqual(join(mnum(10), mnum(-0.5)), -10.5)
        self.assertEqual(join(mnum(0.5), (mnum(5))), 5.5)
        self.assertEqual(join(mnum(-0.5), (mnum(5))), -5.5)
        self.assertEqual(join(mnum('-0.5'), (mnum('0.5'))), mnum('-0.55'))
        self.assertEqual(join(mnum('-0.5'), (mnum('0.56'))), mnum('-0.556'))

    def test_iter(self) -> None:
        self.assertEqual(list(mnum('0')), [0])
        self.assertEqual(list(mnum('-1')), [-1])
        self.assertEqual(list(mnum('1.0')), [1, 0])
        self.assertEqual(list(mnum('0.1')), [0, 1])
        self.assertEqual(list(mnum('-1.0')), [-1, 0])
        self.assertEqual(list(mnum('10')), [1, 0])
        self.assertEqual(list(mnum('100')), [1, 0, 0])
        self.assertEqual(list(mnum('-111')), [-1, -1, -1])

    def test_reverse_iter(self) -> None:
        self.assertEqual(list(reversed(mnum('0'))), [0])
        self.assertEqual(list(reversed(mnum('-1'))), [-1])
        self.assertEqual(list(reversed(mnum('0.1'))), [1, 0])
        self.assertEqual(list(reversed(mnum('1.0'))), [0, 1])
        self.assertEqual(list(reversed(mnum('-1.0'))), [0, -1])
        self.assertEqual(list(reversed(mnum('10'))), [0, 1])
        self.assertEqual(list(reversed(mnum('100'))), [0, 0, 1])
        self.assertEqual(list(reversed(mnum('-111'))), [-1, -1, -1])

    def test_int_len(self) -> None:
        self.assertEqual(mnum('0').int_len(), 1)
        self.assertEqual(mnum('0.0').int_len(), 1)
        self.assertEqual(mnum('0.5').int_len(), 1)
        self.assertEqual(mnum('1').int_len(), 1)
        self.assertEqual(mnum('1.0').int_len(), 1)
        self.assertEqual(mnum('1.5').int_len(), 1)
        self.assertEqual(mnum('0.01').int_len(), 1)
        self.assertEqual(mnum('0.0001').int_len(), 1)
        self.assertEqual(mnum('256.01').int_len(), 3)
        self.assertEqual(mnum('25689.01').int_len(), 5)
        self.assertEqual(mnum('-256890.01').int_len(), 6)

    def test_frac_len(self) -> None:
        self.assertEqual(mnum('0').frac_len(), 0)
        self.assertEqual(mnum('0.0').frac_len(), 1)
        self.assertEqual(mnum('0.5').frac_len(), 1)
        self.assertEqual(mnum('1').frac_len(), 0)
        self.assertEqual(mnum('1.0').frac_len(), 1)
        self.assertEqual(mnum('1.5').frac_len(), 1)
        self.assertEqual(mnum('256.01').frac_len(), 2)
        self.assertEqual(mnum('25689.0156').frac_len(), 4)
        self.assertEqual(mnum('-25680.01569').frac_len(), 5)

    def test_len(self) -> None:
        self.assertEqual(len(mnum('0')), 1)
        self.assertEqual(len(mnum('0.0')), 2)
        self.assertEqual(len(mnum('0.5')), 2)
        self.assertEqual(len(mnum('1')), 1)
        self.assertEqual(len(mnum('1.0')), 2)
        self.assertEqual(len(mnum('1.5')), 2)
        self.assertEqual(len(mnum('256.01')), 5)
        self.assertEqual(len(mnum('25689.0156')), 9)
        self.assertEqual(len(mnum('-25680.01569')), 10)

    def test_convert(self) -> None:
        self.assertEqual(mnum('0').as_int(), 0)
        self.assertEqual(mnum('1').as_int(), 1)
        self.assertEqual(mnum('0.1').as_int(), 0)
        self.assertEqual(mnum('1.0').as_int(), 1)
        self.assertEqual(mnum('1.5').as_int(), 1)
        self.assertEqual(mnum('-1.0').as_int(), -1)
        self.assertEqual(mnum('-1.5').as_int(), -1)
        self.assertEqual(mnum('256.01').as_int(), 256)
        self.assertEqual(mnum('25689.0156').as_int(), 25689)
        self.assertEqual(mnum('-2568.01569').as_int(), -2568)

        self.assertEqual(mnum('1').as_float(), 0)
        self.assertEqual(mnum('1.0').as_float(), 0)
        self.assertEqual(mnum('1.5').as_float(), 0.5)
        self.assertEqual(mnum('-1.0').as_float(), -0.0)
        self.assertEqual(mnum('-1.5').as_float(), -0.5)
        self.assertEqual(mnum('256.01').as_float(), mnum('0.01'))
        self.assertEqual(mnum('25689.0156').as_float(), mnum('0.0156'))
        self.assertEqual(mnum('-2568.01569').as_float(), mnum('-0.01569'))

        self.assertEqual(mnum('1').frac_part(), 0)
        self.assertEqual(mnum('1.0').frac_part(), 0)
        self.assertEqual(mnum('1.5').frac_part(), 5)
        self.assertEqual(mnum('-1.0').frac_part(), 0)
        self.assertEqual(mnum('-1.5').frac_part(), -5)
        self.assertEqual(mnum('256.01').frac_part(), 1)
        self.assertEqual(mnum('25689.0156').frac_part(), 156)
        self.assertEqual(mnum('-2568.01569').frac_part(), -1569)

        self.assertEqual(str(mnum('1')), '1')
        self.assertEqual(str(mnum('1.0')), '1.0')
        self.assertEqual(str(mnum('-1.0')), '-1.0')
        self.assertEqual(str(mnum('-1.5')), '-1.5')

        self.assertEqual(mnum('1').float_str(), '1.0')
        self.assertEqual(mnum('-1').float_str(), '-1.0')
        self.assertEqual(mnum('-1.0').float_str(), '-1.0')
        self.assertEqual(mnum('-1.5').float_str(), '-1.5')


if __name__ == '__main__':
    unittest.main()
