

class MeasurementError(Exception):
    def __init__(self, uom=''):
        self.uom = uom
    def __str__(self):
        if self.uom:
            return f'No such unit of measurement! ({self.uom})'
        return 'No such unit of measurement!'

class TooLittle(Exception):
    def __init__(self, minim=None):
        if minim is None:
            self.minim = 'minimum'
            return
        self.minim = minim
    def __str__(self):
        return f'Given number is less than {self.minim}!'


class TooBig(Exception):
    def __init__(self, maxim=None):
        if maxim is None:
            self.maxim = 'maximum'
            return
        self.maxim = maxim
    def __str__(self):
        return f'Given number is greater than {self.maxim}!'

class WrongDigit(Exception):
    def __init__(self, digit=None):
        self.digit = digit
    def __str__(self):
        if self.digit is None:
            return f"There are digit(s) in value that shouldn't exists in given base."
        return f'"{self.digit}" shouldn\'t exist in given base!'

class NotInPrintable(Exception):
    def __str__(self):
        return f"There are digit(s) in value that printable doesn't contain."