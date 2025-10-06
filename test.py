from string import printable
from Num import Num
from Bytes import *
from constants import true, false

def main():
    a = -Bytes(128)
    print(a.get_auto_scaled())

if __name__ == '__main__':
    main()