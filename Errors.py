

class MeasurementError(Exception):
    def __init__(self, uom=''):
        self.uom = uom
    def __str__(self):
        if self.uom:
            return f'No such unit of measurement! ({self.uom})'
        return 'No such unit of measurement!'
