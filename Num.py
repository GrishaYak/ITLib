from string import printable
from Errors import TooLittle, TooBig, WrongDigit, NotInPrintable

def translate_from_10(num, base):
    """Returns given num in given base as a Num-object
    :param num: int that will be translated
    :param base: the base to convert to. Max - 100."""
    if base >= len(printable):
        raise TooBig(100)
    if base < 1:
        raise TooLittle(1)
    res = ''
    sgn = '-' if num < 0 else ''
    num = abs(num)
    while num!=0:
        res += printable[num % base]
        num//=base
    res = res[::-1]
    res = sgn + res
    return Num(res, base)

def convert_to_num(value):
    """Returns Num that responds to given value
    :param value: int, float, bool or even Num"""
    if isinstance(value, float) or isinstance(value, bool):
        value = int(value)
    if isinstance(value, int):
        value = Num(value)
    return value


class Num:
    def __init__(self, value, base=10):
        """
        If value is int or float, then it translates it from 10th to given base.
        If value is string, then it thinks of it as if it was a number in given base.
        If value is Num, then it just makes its copy.
        :param value: either int, float string or Num
        :param base: int
        """
        if isinstance(value, float):
            value = int(value)
        if isinstance(value, int):
            self.value = translate_from_10(value, base)
        if isinstance(value, Num):
            self.value = value.value
            self.base = value.base
            return
        if isinstance(value, str):
            try:
                for char in value:
                    if printable.index(char) >= base:
                        raise WrongDigit(char)
            except ValueError:
                raise NotInPrintable()
            self.value = value

        self.base = base

    def get_int(self):
        """Get a number in decimal notation. You can use \"int(*Num*)\" as well."""
        res = 0
        sign = 1 - 2 * (self.value[0] == '-')
        end = len(self.value) - 1 * (sign < 0)
        for i in range(end):
            el = self.value[-(i + 1)]
            val = printable.index(el)
            res += val * (self.base ** i)
        return res * sign

    def get_in_base(self, base):
        """Returns a number in given base"""
        return translate_from_10(self.get_int(), base)

    def translate_to_base(self, base):
        """Change value according to given base"""
        self.value = self.get_in_base(base)
        self.base = base

    def copy(self):
        return Num(self.value, self.base)

    def __copy__(self):
        return self.copy()

    def __int__(self):
        return self.get_int()

    def __bool__(self):
        return int(self) != 0

    def __float__(self):
        return float(self.get_int())

    def __add__(self, other):
        other = convert_to_num(other)
        summa = self.get_int() + other.get_int()
        return Num(summa, self.base)

    def __sub__(self, other):
        other = convert_to_num(other)
        difference = self.get_int() - other.get_int()
        return Num(difference, self.base)

    def __mul__(self, other):
        other = convert_to_num(other)
        mul = self.get_int() * other.get_int()
        return Num(mul, self.base)

    def __truediv__(self, other):
        other = convert_to_num(other)
        div = self.get_int() // other.get_int()
        return Num(div, self.base)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return Num(-self.get_int(), self.base)

    def __str__(self):
        return f"{self.value} ({self.base})"