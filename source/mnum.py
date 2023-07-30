from decimal import Decimal, getcontext
from typing import TypeAlias, Sequence, Union, Iterator

_Decimal: TypeAlias = Union[Decimal, int]
_Number: TypeAlias = Union['mnum', Decimal, int]
_ComparableNum: TypeAlias = Union[Decimal, int, float]
_DecimalNew: TypeAlias = Union[Decimal, str, float,
                               tuple[int, Sequence[int], int]]


getcontext().prec = 100  # set digits precision to 100
# hopefully it's enough for most calculations otherwise
# application would crash due to IndexError.
# as soon as digits are converted to scientific notation.


class mnum:
    def __init__(self, number: _DecimalNew) -> None:
        self.__number = Decimal(number)

    def __bool__(self) -> bool:
        return bool(self.__number)

    def __eq__(self, value: Union['mnum', _Decimal]) -> bool:
        if isinstance(value, self.__class__):
            return self.__number == value.__number
        elif isinstance(value, int):
            return self.__number == Decimal(value)
        elif isinstance(value, float):
            return self.__number == Decimal(value)
        raise TypeError(f"Cannot compare Number with {type(value)}")

    def __lt__(self, value: Union[_ComparableNum, 'mnum']) -> bool:
        return self.__number < self.__cmp_cast(value)

    def __le__(self, value: Union[_ComparableNum, 'mnum']) -> bool:
        return self.__number <= self.__cmp_cast(value)

    def __gt__(self, value: Union[_ComparableNum, 'mnum']) -> bool:
        return self.__number > self.__cmp_cast(value)

    def __ge__(self, value: Union[_ComparableNum, 'mnum']) -> bool:
        return self.__number >= self.__cmp_cast(value)

    def __cmp_cast(self, value: Union[_ComparableNum, 'mnum']) -> _ComparableNum:
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

    def __add__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number + self.__cast(value))

    def __radd__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) + self.__number)

    def __iadd__(self, value: _Number) -> 'mnum':
        self.__number += self.__cast(value)
        return self

    def __sub__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number - self.__cast(value))

    def __rsub__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) - self.__number)

    def __isub__(self, value: _Number) -> 'mnum':
        self.__number -= self.__cast(value)
        return self

    def __mul__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number * self.__cast(value))

    def __rmul__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) * self.__number)

    def __imul__(self, value: _Number) -> 'mnum':
        self.__number *= self.__cast(value)
        return self

    def __truediv__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number / self.__cast(value))

    def __rtruediv__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) / self.__number)

    def __itruediv__(self, value: _Number) -> 'mnum':
        self.__number /= self.__cast(value)
        return self

    def __floordiv__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number // self.__cast(value))

    def __rfloordiv__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) // self.__number)

    def __ifloordiv__(self, value: _Number) -> 'mnum':
        self.__number //= self.__cast(value)
        return self

    def __mod__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number % self.__cast(value))

    def __rmod__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) % self.__number)

    def __imod__(self, value: _Number) -> 'mnum':
        self.__number %= self.__cast(value)
        return self

    def __pow__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__number ** self.__cast(value))

    def __rpow__(self, value: _Number) -> 'mnum':
        return self.__class__(self.__cast(value) ** self.__number)

    def __cast(self, value: Union[_Decimal, 'mnum']) -> _Decimal:
        return value.__number if isinstance(
            value, self.__class__) else value  # type: ignore

    def __len__(self) -> int:
        return len(self.__number.as_tuple().digits)

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
        return len(decimal_tuple.digits) + int(decimal_tuple.exponent)

    def frac_len(self) -> int:
        return abs(int(self.__number.as_tuple().exponent))

    def add(self, value: 'mnum') -> 'mnum':
        x_decimal_tuple = self.__number.as_tuple()
        y_decimal_tuple = value.__number.as_tuple()
        sign = x_decimal_tuple.sign or y_decimal_tuple.sign
        digits = x_decimal_tuple.digits + y_decimal_tuple.digits
        return self.__class__((sign, digits, int(x_decimal_tuple.exponent)))

    def join(self, value: Union[int, 'mnum']) -> None:
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
        self.__number = Decimal((sign, digits, int(x_decimal_tuple.exponent)))

    def __getitem__(self, index: int) -> 'mnum':
        decimal_tuple = self.__number.as_tuple()
        digit = decimal_tuple.digits[index]
        return self.__class__((decimal_tuple.sign, (digit,), 0))

    def geti(self, index: int) -> Union['mnum', None]:
        decimal_tuple = self.__number.as_tuple()
        int_len = len(decimal_tuple.digits) + int(decimal_tuple.exponent)
        if index < 0:
            index = int_len + index
        if index >= int_len or index < 0:
            return
        return self.__class__((decimal_tuple.sign, (decimal_tuple.digits[index],), 0))

    def getf(self, index: int) -> Union['mnum', None]:
        decimal_tuple = self.__number.as_tuple()
        frac_len = abs(int(decimal_tuple.exponent))
        int_len = len(decimal_tuple.digits) - frac_len
        if frac_len == 0:
            return
        if index < 0:
            index = frac_len + index
        if index >= frac_len or index < 0:
            return
        index = int_len + index
        return self.__class__((decimal_tuple.sign, (decimal_tuple.digits[index],), 0))

    def __iter__(self) -> Iterator['mnum']:
        decimal_tuple = self.__number.as_tuple()
        return (
            self.__class__((decimal_tuple.sign, (digit,), 0))
            for digit in decimal_tuple.digits
        )

    def __reversed__(self) -> Iterator['mnum']:
        decimal_tuple = self.__number.as_tuple()
        digits = decimal_tuple.digits
        yield from (
            self.__class__((decimal_tuple.sign, (digit,), 0))
            for digit in reversed(digits)
        )
        if len(digits) == abs(int(decimal_tuple.exponent)):
            yield self.__class__((decimal_tuple.sign, (0,), 0))

    def float_str(self) -> str:
        num_str = str(self.__number)
        if num_str.rfind('.') != -1:
            return num_str
        return f"{num_str}.0"

    def __repr__(self) -> str:
        return str(self.__number)
