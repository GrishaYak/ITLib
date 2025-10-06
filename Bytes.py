from Errors import MeasurementError
from  constants import ok, units_of_measurement, coefficients_for_units, false, true
from math import ceil

def get_coef(uom:str):
    """Give it the unit of measurement, and it will give you the right coefficient to translate it to bits"""
    k = 1
    for el in uom:
        k *= units_of_measurement[el]
    return k

def check_last(num:int, cnt:int):
    """Checks if last *cnt* digits in binar version of this number are all zeros"""
    for i in range(cnt):
        if num & 1:
            return False
        num >>= 1
    return True

def parse_uom(uom):
    error = MeasurementError(uom)
    if len(uom) > 2 or not uom:
        return error, uom
    if len(uom) == 1:
        if uom not in 'bB':
            return error, uom
        return ok, uom
    if uom[1] not in 'bB' or uom[0].upper() not in units_of_measurement.keys():
        return error, uom
    if uom[0].capitalize() != uom[0]:
        uom = uom.upper()
    return ok, uom


def _parse_other(other):
    if type(other) is bool or type(other) is float:
        other = int(other)
    if type(other) is int:
        return Bytes(other)
    return other


class Bytes:
    def __init__(self, value=0, uom='b', auto_scale=false):
        """
        You can store weight of information here
        :param value: the weight
        :param uom: the unit of measurement
        :param auto_scale: if true, automatically scale the value
        """
        if isinstance(value, Bytes):
            self.value = value.value
            self.uom = value.uom
        else:
            if value == int(value):
                value = int(value)
            code, self.uom = parse_uom(uom)
            if code != ok:
                print(code)
                exit()
            self.value = value
        k = get_coef(self.uom)
        self.value_in_bits = ceil(self.value * k)
        if auto_scale:
            self.auto_scale()

    def __copy__(self):
        return Bytes(self.value, self.uom)

    def copy(self):
        return self.__copy__()

    def get_in(self, uom:str):
        code, uom = parse_uom(uom)
        if code != ok:
            print(code)
            return code
        return Bytes(self.value_in_bits / get_coef(uom), uom)

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
            self.uom = coefficients_for_units[k] + 'B'

    def get_auto_scaled(self):
        res = self.copy()
        res.auto_scale()
        return res

    def __int__(self):
        return int(self.value)

    def __add__(self, other):
        other = _parse_other(other)
        summ = Bytes(self.value_in_bits + other.value_in_bits)
        return summ.get_auto_scaled()

    def __neg__(self):
        return Bytes(-self.value, uom=self.uom)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = _parse_other(other)
        mul = Bytes(self.value_in_bits * other.value_in_bits)
        return mul.get_auto_scaled()

    def __truediv__(self, other):
        other = _parse_other(other)
        div = Bytes(self.value_in_bits / other.value_in_bits)
        return div.get_auto_scaled()


    def __floordiv__(self, other):
        other = _parse_other(other)
        div = Bytes(self.value_in_bits // other.value_in_bits)
        return div.get_auto_scaled()

    def __mod__(self, other):
        other = _parse_other(other)
        mod = Bytes(self.value_in_bits % other.value_in_bits)
        return mod.get_auto_scaled()

    def __str__(self):
        uom = self.uom
        if uom == 'b':
            uom = 'bits'
        if uom == 'B':
            uom = 'bytes'
        return f'{self.value} {uom}'

    def __eq__(self, other):
        other = _parse_other(other)
        return self.value_in_bits == other.value_in_bits

    def __gt__(self, other):
        other = _parse_other(other)
        return self.value_in_bits > other.value_in_bits

    def __lt__(self, other):
        other = _parse_other(other)
        return self.value_in_bits < other.value_in_bits

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other
