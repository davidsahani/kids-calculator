from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import TextField

from maths import add, div, mnum, mul, sub, true_div


class DisplayText:
    def __init__(self) -> None:
        self.__init_attrs()
        self.text_field: 'TextField'

    def __init_attrs(self) -> None:
        self.operator = ''
        self.left_operand = ''
        self.right_operand = ''
        self.left_end_reached = False
        self.right_end_reached = False
        self.left_operand_has_dot = False
        self.right_operand_has_dot = False
        self.calculation_done = False

    def clear(self) -> None:
        self.__init_attrs()
        self.text_field.set_text('')

    def erase_to_left(self) -> None:
        if not self.operator:
            if self.left_operand and self.left_operand[-1] == '.':
                self.left_operand_has_dot = False
            if self.left_operand and self.left_operand[-1] in '+-':
                self.left_operand = self.left_operand[1:]
            self.left_end_reached = False
            self.left_operand = self.left_operand[:-1]
        elif not self.right_operand:
            self.operator = ''
        else:
            if self.right_operand and self.right_operand[-1] == '.':
                self.right_operand_has_dot = False
            if self.right_operand and self.right_operand[-1] in '+-':
                self.right_operand = self.right_operand[1:]
            self.right_end_reached = False
            self.right_operand = self.right_operand[:-1]
        self._update_text()

    def insert_sign(self, sign: str) -> None:
        def change_sign(operand: str) -> str:
            is_sign_neg = operand[0] == '-' \
                if operand else False

            if (
                sign == '-' and is_sign_neg or
                sign == '+' and not is_sign_neg
            ):
                return operand
            elif is_sign_neg:
                return operand[1:]
            else:
                return '-' + operand

        if not self.operator:
            self.left_operand = change_sign(self.left_operand)
        else:
            self.right_operand = change_sign(self.right_operand)

        self._update_text()

    def insert_operator(self, operator: str) -> None:
        if not self.left_operand:
            return
        self.operator = operator
        self._update_text()

    def insert(self, number: str) -> None:
        if not self.operator and not self.left_end_reached:
            if number == '.':
                if self.left_operand_has_dot:
                    return
                if not self.left_operand:
                    self.left_operand = '0'
                self.left_operand_has_dot = True

            self.left_operand += number
            self._update_text()  # update text label

            self.left_end_reached = self.text_field.\
                max_text_size - 4 < len(self.left_operand)
            return

        if self.left_operand[-1] == '.':
            self.left_operand = self.left_operand[:-1]

        if not self.operator:
            return

        if self.right_end_reached:
            return

        if number == '.':
            if self.right_operand_has_dot:
                return
            if not self.right_operand:
                self.right_operand = '0'
            self.right_operand_has_dot = True

        self.right_operand += number
        self._update_text()  # update text label

        self.right_end_reached = self.text_field.max_text_size - 4 < \
            len(self.right_operand) + \
            (0 if self.operator not in '/%' else len(self.right_operand))

    symbols = {'+': '\u002B', '-': '\u2013', '*': '\u00D7', '': ''}

    def _update_text(self) -> None:
        self.calculation_done = False

        if not self.operator or self.operator not in '/%':
            self.text_field.label.halign = 'right'
            self.text_field.set_text(
                '\n' + self.left_operand + ' ' +
                '\n' + self.symbols[self.operator] + ' ' +
                self.right_operand.rjust(len(self.left_operand)) + ' '
            )
            return
        self.text_field.label.halign = 'left'
        upper_bar = f"┌{'─' * (len(self.left_operand) + 1)}\n"
        spacing = ' ' * (len(self.right_operand) + 2)
        text = spacing + upper_bar + \
            f" {self.right_operand} │ {self.left_operand}"
        self.text_field.set_text('\n' + text)

    def show_calculation(self) -> None:
        if self.calculation_done:
            return
        if not self.right_operand:
            return
        if self.right_operand[-1] == '.':
            self.right_operand = self.right_operand[:-1]
            self.right_operand_has_dot = False
            self._update_text()

        self.calculation_done = True

        prev_text = self.text_field.text
        self.text_field.set_text('')
        space = '\u00A0'  # non-breaking space

        num_x = mnum(self.left_operand)
        num_y = mnum(self.right_operand)

        if self.operator in '+-':
            index = self.operator == '-'  # (+, -) => (0, 1)
            result, carries = (add, sub)[index](num_x, num_y)

            # if not all carries are zero
            if any(char == '1' for char in carries):
                self.text_field.set_ctext(
                    carries.replace('0', space).
                    replace('.', space) + space
                )
            # if both operands do not have fractional part
            if num_x.frac_len() == 0 and num_y.frac_len() == 0:
                self.text_field.insert(prev_text)
            else:
                def zfill(number: str, n_zeros: int) -> str:
                    return number + '0' * n_zeros

                max_len = max(num_x.frac_len(), num_y.frac_len())
                opl = zfill(num_x.float_str(), max_len -
                            (num_x.frac_len() or 1))
                opr = zfill(num_y.float_str(), max_len -
                            (num_y.frac_len() or 1))

                self.text_field.insert(
                    '\n' + opl + ' ' + '\n' +
                    self.symbols[self.operator] +
                    ' ' + opr.rjust(len(opl)) + ' '
                )
            self.text_field.insert(
                '\n' + '―' * len(result) + ' \n' + result + ' ')
            return

        if self.operator == '*':
            result, products, carries = mul(num_x, num_y)
            # filter carries with non-zeros
            filtered_carries = f'{space}\n'.join(
                p_carries for p_carries in reversed(carries)
                if not all(char in '.0' for char in p_carries)
            )
            self.text_field.set_ctext(filtered_carries.replace(
                '0', space).replace('.', space) + space + '\n'
            )
            self.text_field.insert(prev_text.lstrip('\n') + '\n')
            bar_and_result = '―' * len(result) + ' \n' + result + ' '
            if len(num_y) == 1:  # if multiplier is of size 1
                self.text_field.insert(bar_and_result)
                return
            self.text_field.insert('―' * max(
                len(self.left_operand), len(self.right_operand)) + ' \n'
            )
            for partial_products in products:
                self.text_field.insert(partial_products + ' \n')
            self.text_field.insert(bar_and_result)
            return

        font_size = self.text_field.label.font_size
        if num_y == 0:
            msg = 'division by zero is not allowed.'
            self.text_field.set_text(
                prev_text +
                f"\n\n\n[size={font_size - 10}] [b]{msg}[/b][/size]"
            )
            return

        dividend, divisor = num_x, num_y
        dividend_frac_len = dividend.frac_len()
        divisor_frac_len = divisor.frac_len()
        has_frac_parts = dividend_frac_len != 0 or divisor_frac_len != 0

        if has_frac_parts:
            # normalize the dividend and divisor
            dividend = dividend.as_int() if dividend_frac_len == 0 else \
                dividend.as_int().add(dividend.frac_part())
            divisor = divisor.as_int() if divisor_frac_len == 0 else \
                divisor.as_int().add(divisor.frac_part())

            if dividend_frac_len < divisor_frac_len:  # normalize denominator
                for _ in range(divisor_frac_len - dividend_frac_len):
                    dividend.join(0)
            elif dividend_frac_len > divisor_frac_len:  # normalize nominator
                for _ in range(dividend_frac_len - divisor_frac_len):
                    divisor.join(0)

            next_line = '' if len(self.left_operand) + \
                len(self.right_operand) < 20 else '\n\n'

            steps = (
                " Step 1: Normalize denominator and nominator",
                f" {self.left_operand} / {self.right_operand}" +
                f"{next_line} => {dividend} / {divisor}",
                " Step 2: Perform division"
            )
            text = '\n\n'.join(steps) + '\n'
            self.text_field.set_text(f"[size={font_size - 12}]{text}[/size]\n")

        if self.operator == '/':
            max_text = self.text_field.max_text_size - 6
            opr_len = len(self.right_operand)
            precision = max((max_text * 2) - opr_len, max_text)

            result = true_div(dividend, divisor, precision)
            self._show_division(dividend, divisor, *result)
            return

        result = div(dividend, divisor)
        self._show_division(dividend, divisor, *result)

        def insert(text: str) -> None:
            self.text_field.insert(
                f"\n[size={font_size - 10}] {text}[/size]"
            )

        quot = mnum(result[0])
        rem = num_x - num_y * quot
        insert("\n\n Using formula: r = n - pq")
        insert(f"r = {num_x} - ({num_y} x {quot}) => {rem}")
        insert(f"Thus remainder is: {rem}")

    def _show_division(self, dividend: mnum, divisor: mnum, quotient: str,
                       term_minuses: list[mnum], minus_terms: list[mnum], remainders: list[mnum]) -> None:

        divisor_str = str(divisor)
        dividend_str = str(dividend)
        divisor_len = len(divisor_str)

        spacing = ' ' * (divisor_len + 2)
        bar_len = max(len(dividend_str), len(quotient)) + 1
        header_text = spacing + f"┌{'─' * bar_len}\n" + \
            f" {divisor} │ {dividend_str}"

        self.text_field.insert(
            (' ' if quotient[0] == '-' and dividend > 0 else '  ')
            + spacing + quotient + '\n' + header_text
        )
        spacing = ' ' * (divisor_len + 3 + (1 if dividend < 0 else 0))
        font_size = self.text_field.label.font_size

        division_steps: list[str] = []

        def append(text: str) -> None:
            division_steps.append(f"\n[size={font_size - 1}]{text}[/size]")

        # append the division steps
        for term_minus, minus_term, remainder in zip(term_minuses, minus_terms, remainders):
            term_minus_str = str(term_minus)
            minus_term_str = str(abs(minus_term))

            minus_term_len = len(minus_term_str)
            term_minus_len = len(term_minus_str) - (term_minus < 0)
            bar_len = max(term_minus_len, minus_term_len)
            minus_term_sign = '+' if minus_term < 0 else '-'

            append(f"{spacing} {'─' * bar_len}")
            append(f"{spacing}{' ' if term_minus >= 0 else ''}{term_minus_str}")
            m_term = minus_term_str.rjust(len(minus_term) - (term_minus > 0))
            append(f"{spacing}{minus_term_sign}{m_term}")
            append(f"{spacing} {'─' * bar_len}")
            append(f"{spacing}{'' if remainder < 0 else ' '}{remainder}")

        self.text_field.insert(''.join(division_steps))
