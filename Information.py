from Errors import MeasurementError

units = {'T': 1<<40,'G': 1<<30, 'M':1<<20, 'K':1<<10, 'B':1<<3, 'b': 1}
coeffs = {1 << 40: 'T', 1 << 30: 'G', 1 << 20: 'M', 1 << 10: 'K', 1 << 3: 'B', 1: 'b'}


def get_coef(uom:str):
    """Give it the unit of measurement, and it will give you the right coefficient to translate it to bits"""
    k = 1
    for el in uom:
        if el not in units:
            raise MeasurementError(uom)
        k *= units[el]
    return k

def check_last(num:int, cnt:int):
    """Checks if last *cnt* digits in binar version of this number are all zeros"""
    for i in range(cnt):
        if num & 1:
            return False
        num >>= 1
    return True


class Information:
    def __init__(self, value, uom='b'):
        """
        You can store weight of information here
        :param value: the weight
        :param uom: the unit of measurement
        """
        try:
            k = get_coef(uom)
        except MeasurementError as e:
            print(e)
            exit()
        self.value = value
        self.value_in_bits = value * k
        self.uom = uom

    def __copy__(self):
        return Information(self.value, self.uom)

    def copy(self):
        return self.__copy__()

    def get_in(self, uom:str):
        if self.uom == uom:
            return self.value
        try:
            k = get_coef(uom)
        except MeasurementError as e:
            print(e)
            return e
        return self.value_in_bits / k

    def translate_to(self, uom:str):
        val = self.get_in(uom)
        if val == MeasurementError().__str__():
            exit()
        self.value = val
        self.uom = uom

    def auto_scale(self):
        if self.value != int(self.value):
            return
        self.value = int(self.value)
        if len(self.uom) == 1:
            if self.uom == 'b':
                if check_last(self.value, 3):
                    self.value >>= 3
                    self.uom = 'B'
                else:
                    return
            if self.uom == 'B':
                if check_last(self.value, 10):
                    self.value >>= 10
                    self.uom = 'KB'
                else:
                    return
        else:
            if self.uom[1] == 'b':
                if check_last(self.value, 3):
                    self.value >>= 3
                    self.uom = self.uom[0] + 'B'
                else:
                    return
        while check_last(self.value, 10):
            self.value >>= 10
            k = get_coef(self.uom[0])
            k <<= 10
            self.uom = coeffs[k] + 'B'

    def get_auto_scaled(self):
        res = self.copy()
        res.auto_scale()
        return res

    def __add__(self, other):
        summ = Information(self.value_in_bits + other.value_in_bits)
        return summ.get_auto_scaled()

    def __neg__(self):
        return Information(-self.value_in_bits, uom=self.uom)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        mul = Information(self.value_in_bits * other.value_in_bits)
        return mul.get_auto_scaled()

    def __truediv__(self, other):
        div = Information(self.value_in_bits / other.value_in_bits)
        return div.get_auto_scaled()

    def __floordiv__(self, other):
        div = Information(self.value_in_bits // other.value_in_bits)
        return div.get_auto_scaled()

    def __mod__(self, other):
        mod = Information(self.value_in_bits % other.value_in_bits)
        return mod.get_auto_scaled()

    def __str__(self):
        return f'{self.value} {self.uom}'