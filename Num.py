def translate_from_10(num, base):
    """Returns given num in given base as string"""
    res = ''
    if num < 0:
        sgn = -1
        num *= sgn
    else:
        sgn=1
    while num!=0:
        digit = num % base
        if digit >=10:
            digit = chr(ord('a') + digit - 10)
        res += f'{digit}'
        num//=base
    res = res[::-1]
    if sgn < 0:
        res = '-' + res
    return res

def Num_from_int(n:int, base:int):
    """Get a Num object from a decimal num (int) and base (int)"""
    return Num(translate_from_10(n, base), base)

class Num:
    def __init__(self, value, base=10):
        self.value = value
        self.base = base

    def get_int(self):
        """Get a number in decimal notation"""
        res = 0
        sign = 1 - 2 * (self.value[0] == '-')
        end = len(self.value) - 1 * (sign < 0)
        for i in range(end):
            el = self.value[-(i + 1)]
            if el.isdigit():
                val = int(el)
            else:
                val = ord(el) - ord('a') + 10
            res += val * (self.base ** i)
        return res * sign

    def get_in_base(self, base):
        """Get a number in given base"""
        return translate_from_10(self.get_int(), base)

    def translate_to_base(self, base):
        """Change value according to given base"""
        self.value = self.get_in_base(base)
        self.base = base

    def __add__(self, other):
        summa = self.get_int() + other.get_int()
        return Num_from_int(summa, self.base)

    def __sub__(self, other):
        difference = self.get_int() - other.get_int()
        return Num_from_int(difference, self.base)

    def __mul__(self, other):
        mul = self.get_int() * other.get_int()
        return Num_from_int(mul, self.base)

    def __truediv__(self, other):
        div = self.get_int() // other.get_int()
        return Num_from_int(div, self.base)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return Num_from_int(-self.get_int(), self.base)

    def __str__(self):
        return f"{self.value} ({self.base})"