
from machine import UART
import time
import binascii


uart = UART(2, 9600, tx=17, rx=16)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

print("Hello")

while True:
    resp = uart.readline()
    if resp:
        # resp = binascii.hexlify(resp).decode()
        print(resp.split()[1].decode(), "kg")
        time.sleep(.3)
