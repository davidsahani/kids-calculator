from decimal import Decimal, getcontext
from typing import TYPE_CHECKING, Iterator, TypeAlias

if TYPE_CHECKING:
    from _decimal import _ComparableNum, _Decimal, _DecimalNew  # type: ignore

_Number: TypeAlias = 'mnum | _Decimal'


getcontext().prec = 100  # set digits precision to 100
# hopefully it's enough for most calculations otherwise
# application would crash due to IndexError.
# as soon as digits are converted to scientific notation.


class mnum:
    def __init__(self, number: '_DecimalNew') -> None:
        self.__number = Decimal(number)

    def __bool__(self) -> bool:
        return bool(self.__number)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__number == value.__number
        elif isinstance(value, (int, float)):
            return self.__number == Decimal(value)
        else:
            return False

    def __lt__(self, value: 'mnum | _ComparableNum') -> bool:
        return self.__number < self.__cmp_cast(value)

    def __le__(self, value: 'mnum | _ComparableNum') -> bool:
        return self.__number <= self.__cmp_cast(value)

    def __gt__(self, value: 'mnum | _ComparableNum') -> bool:
        return self.__number > self.__cmp_cast(value)

    def __ge__(self, value: 'mnum | _ComparableNum') -> bool:
        return self.__number >= self.__cmp_cast(value)

    def __cmp_cast(self, value: 'mnum | _ComparableNum') -> '_ComparableNum':
        return value.__number if isinstance(
            value, self.__class__) else value  # type: ignore

    def __pos__(self) -> 'mnum':
        return self.__class__(+self.__number)

    def __neg__(self) -> 'mnum':
        return self.__class__(-self.__number)

    def __abs__(self) -> 'mnum':
        return self.__class__(abs(self.__number))

    def __int__(self) -> int:
        return int(self.__number)

    def __float__(self) -> float:
        return float(self.__number)

    def __add__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number + self.__cast(value))

    def __radd__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) + self.__number)

    def __iadd__(self, value: '_Number') -> 'mnum':
        self.__number += self.__cast(value)
        return self

    def __sub__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number - self.__cast(value))

    def __rsub__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) - self.__number)

    def __isub__(self, value: '_Number') -> 'mnum':
        self.__number -= self.__cast(value)
        return self

    def __mul__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number * self.__cast(value))

    def __rmul__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) * self.__number)

    def __imul__(self, value: '_Number') -> 'mnum':
        self.__number *= self.__cast(value)
        return self

    def __truediv__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number / self.__cast(value))

    def __rtruediv__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) / self.__number)

    def __itruediv__(self, value: '_Number') -> 'mnum':
        self.__number /= self.__cast(value)
        return self

    def __floordiv__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number // self.__cast(value))

    def __rfloordiv__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) // self.__number)

    def __ifloordiv__(self, value: '_Number') -> 'mnum':
        self.__number //= self.__cast(value)
        return self

    def __mod__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number % self.__cast(value))

    def __rmod__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) % self.__number)

    def __imod__(self, value: '_Number') -> 'mnum':
        self.__number %= self.__cast(value)
        return self

    def __pow__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__number ** self.__cast(value))

    def __rpow__(self, value: '_Number') -> 'mnum':
        return self.__class__(self.__cast(value) ** self.__number)

    def __cast(self, value: '_Decimal | mnum') -> '_Decimal':
        return value.__number if isinstance(
            value, self.__class__) else value  # type: ignore

    def __len__(self) -> int:
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        return max(len(decimal_tuple.digits) + exponent, 1) + abs(exponent)

    def as_int(self) -> 'mnum':
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        if exponent < 0:
            digits = decimal_tuple.digits[:exponent]
        else:
            digits = decimal_tuple.digits
        return self.__class__((decimal_tuple.sign, digits, 0))

    def as_float(self) -> 'mnum':
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        if exponent < 0:
            digits = decimal_tuple.digits[exponent:]
        else:
            digits = (0,)
        return self.__class__((decimal_tuple.sign, digits, exponent))

    def int_part(self) -> 'mnum':
        return self.as_int()

    def frac_part(self) -> 'mnum':
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        if exponent < 0:
            digits = decimal_tuple.digits[exponent:]
        else:
            digits = (0,)
        return self.__class__((decimal_tuple.sign, digits, 0))

    def int_len(self) -> int:
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        return max(len(decimal_tuple.digits) + exponent, 1)

    def frac_len(self) -> int:
        return abs(int(self.__number.as_tuple().exponent))

    def add(self, value: 'mnum') -> 'mnum':
        x_decimal_tuple = self.__number.as_tuple()
        y_decimal_tuple = value.__number.as_tuple()
        sign = x_decimal_tuple.sign or y_decimal_tuple.sign
        digits = x_decimal_tuple.digits + y_decimal_tuple.digits
        exponent = int(x_decimal_tuple.exponent) + \
            int(y_decimal_tuple.exponent)
        return self.__class__((sign, digits, exponent))

    def join(self, value: 'mnum | int') -> None:
        x_decimal_tuple = self.__number.as_tuple()
        if isinstance(value, int):
            if x_decimal_tuple.exponent == 0:
                abs_value = abs(value)
                if abs_value < 10:  # single digit
                    res = abs(self.__number) * 10 + abs_value
                    self.__number = -res if self.__number < 0 \
                        or value < 0 else res
                    return
            value = self.__class__(value)
        y_decimal_tuple = value.__number.as_tuple()
        sign = x_decimal_tuple.sign or y_decimal_tuple.sign
        digits = x_decimal_tuple.digits + y_decimal_tuple.digits
        exponent = int(x_decimal_tuple.exponent) + \
            int(y_decimal_tuple.exponent)
        self.__number = Decimal((sign, digits, exponent))

    def __getitem__(self, index: int) -> 'mnum':
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        int_len = max(len(decimal_tuple.digits) + exponent, 1)
        length = int_len + abs(exponent)
        idx = index + length if index < 0 else index
        if idx >= length or idx < 0:
            raise IndexError("Index out of range")
        if exponent < 0:
            digits = (decimal_tuple.digits[:exponent] or (0,)) + \
                (decimal_tuple.digits[exponent:] or (0,))
        else:
            digits = decimal_tuple.digits
        return self.__class__((decimal_tuple.sign, (digits[idx],), 0))

    def geti(self, index: int) -> 'mnum | None':
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        int_len = max(len(decimal_tuple.digits) + exponent, 1)
        idx = index + int_len if index < 0 else index
        if idx >= int_len or idx < 0:
            return
        if exponent < 0:
            digits = decimal_tuple.digits[:exponent] or (0,)
        else:
            digits = decimal_tuple.digits
        return self.__class__((decimal_tuple.sign, (digits[idx],), 0))

    def getf(self, index: int) -> 'mnum | None':
        decimal_tuple = self.__number.as_tuple()
        if decimal_tuple.exponent == 0:
            return
        exponent = int(decimal_tuple.exponent)
        frac_len = abs(exponent)
        if index < 0:
            index += frac_len
        if index >= frac_len or index < 0:
            return
        if exponent < 0:
            digits = decimal_tuple.digits[exponent:] or (0,)
        else:
            digits = (0,)
        return self.__class__((decimal_tuple.sign, (digits[index],), 0))

    def __iter__(self) -> Iterator['mnum']:
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        return (
            self.__class__((decimal_tuple.sign, (digit,), 0))
            for digit in (
                decimal_tuple.digits if exponent >= 0 else
                (decimal_tuple.digits[:exponent] or (0,)) +
                (decimal_tuple.digits[exponent:] or (0,))
            )
        )

    def __reversed__(self) -> Iterator['mnum']:
        decimal_tuple = self.__number.as_tuple()
        exponent = int(decimal_tuple.exponent)
        return (
            self.__class__((decimal_tuple.sign, (digit,), 0))
            for digit in reversed(
                decimal_tuple.digits if exponent >= 0 else
                (decimal_tuple.digits[:exponent] or (0,)) +
                (decimal_tuple.digits[exponent:] or (0,))
            )
        )

    def float_str(self) -> str:
        num_str = str(self.__number)
        if num_str.rfind('.') != -1:
            return num_str
        return f"{num_str}.0"

    def __repr__(self) -> str:
        return str(self.__number)
