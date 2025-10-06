from Bytes import Bytes
from math import ceil

class Picture:
    def __init__(self, resolution=-1, colors=-1, weight=-1, pixel=-1, k=1, b=0, h=-1, w=-1, total_weight=-1):
        """
        :param resolution: The number of pixels in the picture
        :param colors: Number of possible colors in picture's palette
        :param weight: The weight of one picture ("Bytes" support)
        :param pixel: Count of bits to store one pixel ("Bytes" support)
        :param k: Count of pictures
        :param b: Weight of a header ("Bytes" support)
        :param h: Height of picture (in pixels)
        :param w: Width of picture (in pixels)
        :param total_weight: Weight of all given files together (=k(weight+b)) ("Bytes" support)
        """
        self.h = h
        self.w = w
        if resolution != -1:
            self.resolution = resolution
        else:
            self.resolution = h * w
        self.colors = colors
        self.weight = weight
        self.pixel = pixel
        self.total_weight = total_weight
        self.k = k
        self.b = b
        self._count_all()

    def _count_all(self):
        self._count_colors()
        self._count_pixel()
        self._count_weight()
        self._count_total_weight()

    def _count_colors(self):
        if self.pixel != -1:
            self.colors = 1 << self.pixel
            return
        if self.weight != -1 and self.resolution != -1:
            self.pixel = ceil(self.weight.value_in_bits / self.resolution)
            self.colors = 1 << self.pixel

    def _count_pixel(self):
        if self.pixel != -1:
            return
        if self.colors == -1:
            return
        colors = self.colors
        log = Bytes()
        up = False
        while colors != 1:
            up = up or (colors & 1)
            log += 1
            colors = colors >> 1
        log += up
        self.pixel = log

    def _count_weight(self):
        if self.pixel == -1 or self.resolution == -1:
            return
        self.weight = Bytes(self.pixel * self.resolution)

    def _count_total_weight(self):
        if self.weight == -1:
            return
        self.total_weight = Bytes((self.weight + self.b) * self.k)




