from collections import deque

from mnum import mnum


def _add(augend: mnum, addend: mnum) -> tuple[str, str]:
    assert augend >= 0 and addend >= 0, "Both numbers must be positive"

    carry: int = 0
    int_carries: deque[int] = deque()
    frac_carries: deque[int] = deque()
    int_result: deque[mnum] = deque()
    frac_result: deque[mnum] = deque()

    # perform fractional addition
    for idx in range(max(augend.frac_len(), addend.frac_len()) - 1, -1, -1):
        frac_carries.appendleft(carry)
        nx = augend.getf(idx) or mnum(0)
        ny = addend.getf(idx) or mnum(0)
        res = nx + ny + carry
        if res > 9:
            res -= 10
            carry = 1
        else:
            carry = 0
        frac_result.appendleft(res)

    # perform integer addition
    for idx in range(1, max(augend.int_len(), addend.int_len()) + 1):
        int_carries.appendleft(carry)
        nx = augend.geti(-idx) or mnum(0)
        ny = addend.geti(-idx) or mnum(0)
        res = nx + ny + carry
        if res > 9:
            res -= 10
            carry = 1
        else:
            carry = 0
        int_result.appendleft(res)

    if carry == 1:  # if there's a carry
        int_result.appendleft(mnum(carry))

    result = ''.join(map(str, int_result)) + (
        '.' + ''.join(map(str, frac_result)) if frac_result else ''
    )
    carries = ''.join(map(str, int_carries)) + (
        '.' + ''.join(map(str, frac_carries)) if frac_carries else ''
    )
    return result, carries


def _sub(minuend: mnum, subtrahend: mnum) -> tuple[str, str]:
    assert minuend >= 0 and subtrahend >= 0, "Both numbers must be positive"
    assert minuend >= subtrahend, "Minuend must be greater than or equal to subtrahend"

    borrow: int = 0
    int_borrows: deque[int] = deque()
    frac_borrows: deque[int] = deque()
    int_result: deque[mnum] = deque()
    frac_result: deque[mnum] = deque()

    # perform fractional subtraction
    for idx in range(max(minuend.frac_len(), subtrahend.frac_len()) - 1, -1, -1):
        frac_borrows.appendleft(borrow)
        nx = minuend.getf(idx) or mnum(0)
        ny = subtrahend.getf(idx) or mnum(0)
        res = nx - ny - borrow
        if res < 0:
            res += 10
            borrow = 1
        else:
            borrow = 0
        frac_result.appendleft(res)

    # perform integer subtraction
    for idx in range(1, max(minuend.int_len(), subtrahend.int_len()) + 1):
        int_borrows.appendleft(borrow)
        nx = minuend.geti(-idx) or mnum(0)
        ny = subtrahend.geti(-idx) or mnum(0)
        res = nx - ny - borrow
        if res < 0:
            res += 10
            borrow = 1
        else:
            borrow = 0
        int_result.appendleft(res)

    assert borrow == 0, "Borrow must be zero"

    result = ''.join(map(str, int_result)) + (
        '.' + ''.join(map(str, frac_result)) if frac_result else ''
    )
    borrows = ''.join(map(str, int_borrows)) + (
        '.' + ''.join(map(str, frac_borrows)) if frac_borrows else ''
    )
    return result, borrows


def add(augend: mnum, addend: mnum) -> tuple[str, str]:
    """Perform numeric addition

    Args:
        augend: The first number to be added
        addend: The second number to be added

    Return:
        result, carries
    """
    sign = (augend < 0) + (addend < 0)
    abs_x, abs_y = abs(augend), abs(addend)

    if sign == 0:  # both +ve
        return _add(abs_x, abs_y)
    if sign == 2:  # both -ve
        res, carries = _add(abs_x, abs_y)
        return '-' + res, carries

    # subtract, sign => 1 ; any -ve
    if augend == addend:
        neg_sign = False
    elif abs_x < abs_y:
        abs_x, abs_y = abs_y, abs_x
        neg_sign = augend >= 0 and addend < 0
    else:
        neg_sign = augend < 0 and addend >= 0

    res, carries = _sub(abs_x, abs_y)
    return '-' + res if neg_sign else res, carries


def sub(subtrahend: mnum, minuend: mnum) -> tuple[str, str]:
    """Perform numeric subtraction

    Args:
        subtrahend: The first number to be subtracted
        minuend: The second number to be subtracted

    Return:
        result, borrows
    """
    sign = (subtrahend < 0) + (minuend < 0)
    abs_x, abs_y = abs(subtrahend), abs(minuend)

    if sign == 1:  # any -ve
        res, carries = _add(abs_x, abs_y)
        sym = '-' if subtrahend < 0 else ''
        return sym + res, carries

    # subtract, sign => 0 or 2 ; both +ve or both -ve
    if subtrahend == minuend:
        neg_sign = False
    elif abs_x < abs_y:
        abs_x, abs_y = abs_y, abs_x
        neg_sign = subtrahend >= 0 and minuend >= 0
    else:
        neg_sign = subtrahend < 0 and minuend < 0

    res, carries = _sub(abs_x, abs_y)
    return '-' + res if neg_sign else res, carries


def mul(multiplicand: mnum, multiplier: mnum) -> tuple[str, list[str], list[str]]:
    """Perform numeric multiplication

    Args:
        multiplicand: The first number to be multiplied
        multiplier: The second number to be multiplied

    Return:
        result, products, carries
    """
    placeholder_zeros: int = 0
    carries: deque[deque[mnum]] = deque()
    products: deque[deque[mnum]] = deque()

    for ny in reversed(abs(multiplier)):
        carry: mnum = mnum(0)
        partial_carries: deque[mnum] = deque()
        partial_products: deque[mnum] = deque()

        for idx, nx in enumerate(reversed(abs(multiplicand))):
            partial_carries.appendleft(carry)
            res = nx * ny + carry
            if res > 9:
                carry = res // 10
                res = res % 10
            else:
                carry = mnum(0)
            partial_products.appendleft(res)

        if carry:  # if last product had carry
            partial_products.appendleft(carry)

        # add placeholder zeros to partial products
        zeros = [mnum(0)] * placeholder_zeros
        partial_products.extend(zeros)
        placeholder_zeros += 1

        carries.append(partial_carries)
        products.append(partial_products)

    # sum the partial products
    carry: mnum = mnum(0)
    products_sum: deque[str] = deque()
    for idx in range(-1, -(len(max(products, key=len)) + 1), -1):
        prods_sum: mnum = mnum(0)
        for product in products:
            try:
                value = product[idx]
            except IndexError:
                value = mnum(0)
            prods_sum += value
        prods_sum += carry
        if prods_sum < 10:
            carry = mnum(0)
        else:
            carry = prods_sum // 10
            prods_sum = prods_sum % 10
        products_sum.appendleft(str(prods_sum))
    if carry:  # if last sum had carry
        products_sum.appendleft(str(carry))

    # insert dot symbols for carries
    multiplicand_frac_len = multiplicand.frac_len()
    if multiplicand_frac_len != 0:
        frac_point = multiplicand.int_len()
        for partial_carries in carries:
            partial_carries.insert(frac_point, '.')  # type: ignore

    # insert fraction dot symbol for products_sum
    fractions_len = multiplicand_frac_len + multiplier.frac_len()
    if fractions_len != 0:
        frac_point = len(products_sum) - fractions_len
        products_sum.insert(frac_point, '.')

    sign = (multiplicand < 0) + (multiplier < 0)
    symbol = '-' if sign == 1 else ''  # sign => 1 ; any -ve
    return symbol + ''.join(products_sum), \
        [''.join(map(str, p)) for p in products], \
        [''.join(map(str, c)) for c in carries]


def div(dividend: mnum, divisor: mnum) -> tuple[str, list[mnum], list[mnum], list[mnum]]:
    """Perform numeric integer division

    Args:
        dividend: The number to be divided
        divisor: The number to divide with

    Return:
        quotient, term_minuses, minus_terms, remainders
    """
    assert dividend.frac_len() == 0 and divisor.frac_len() == 0, \
        "dividend and divisor must be integers"

    quotient: list[str] = []
    term_minuses: list[mnum] = []
    minus_terms: list[mnum] = []
    remainders: list[mnum] = []
    remainder: mnum = mnum(0)

    abs_divisor = abs(divisor)
    last_idx = len(dividend) - 1
    is_initials_zero = last_idx != 0

    for idx, div_term in enumerate(dividend):
        term_minus = remainder * 10 + div_term
        quot_div = term_minus // divisor
        minus_term = divisor * quot_div
        remainder = term_minus - minus_term

        # avoid appending unnecessary steps
        if is_initials_zero:
            if quot_div == 0 and idx != last_idx:
                continue  # skip initial quotient zeros
            is_initials_zero = False
        elif quotient and abs(term_minus) + abs(minus_term) < abs_divisor:
            quotient.append(str(abs(quot_div)))
            continue  # skip ignorable intermediate steps

        quotient.append(str(abs(quot_div)))
        term_minuses.append(term_minus)
        minus_terms.append(minus_term)
        remainders.append(remainder)

    sign = '-' if (dividend < 0) + (divisor < 0) == 1 else ''  # 1 (any -ve)
    return sign + ''.join(quotient), term_minuses, minus_terms, remainders


def true_div(dividend: mnum, divisor: mnum, precision: int) -> tuple[str, list[mnum], list[mnum], list[mnum]]:
    """Perform numeric integer division

    Args:
        dividend: The number to be divided
        divisor: The number to divide with

    Return:
        quotient, term_minuses, minus_terms, remainders
    """
    assert dividend.frac_len() == 0 and divisor.frac_len() == 0, \
        "dividend and divisor must be integers"

    quotient: list[str] = []
    term_minuses: list[mnum] = []
    minus_terms: list[mnum] = []
    remainders: list[mnum] = []
    remainder: mnum = mnum(0)

    abs_divisor = abs(divisor)
    is_initials_zero = dividend != 0

    for div_term in dividend:
        term_minus = remainder * 10 + div_term
        quot_div = term_minus // divisor
        minus_term = divisor * quot_div
        remainder = term_minus - minus_term

        # avoid appending unnecessary steps
        if is_initials_zero:
            if quot_div == 0:
                continue  # skip initial quotient zeros
            is_initials_zero = False
        elif quotient and abs(term_minus) + abs(minus_term) < abs_divisor:
            quotient.append(str(abs(quot_div)))
            continue  # skip ignorable intermediate steps

        quotient.append(str(abs(quot_div)))
        term_minuses.append(term_minus)
        minus_terms.append(minus_term)
        remainders.append(remainder)

    if remainder != 0:  # if didn't reach exact division
        quotient.append('.' if quotient else '0.')

    for _ in range(precision):
        if remainder == 0:
            break  # reached exact division
        term_minus = remainder * 10
        quot_div = term_minus // divisor
        minus_term = divisor * quot_div
        remainder = term_minus - minus_term

        # avoid appending unnecessary steps
        if abs(term_minus) + abs(minus_term) < abs_divisor:
            quotient.append(str(abs(quot_div)))
            continue  # skip ignorable intermediate steps

        quotient.append(str(abs(quot_div)))
        term_minuses.append(term_minus)
        minus_terms.append(minus_term)
        remainders.append(remainder)

    sign = '-' if (dividend < 0) + (divisor < 0) == 1 else ''  # 1 (any -ve)
    return sign + ''.join(quotient), term_minuses, minus_terms, remainders
