from ble import BLE
from machine import UART
from time import sleep_ms

ble_obj = BLE("ESP32dav")

uart = UART(2, 9600, tx=17, rx=16)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

while True:
    resp = uart.readline()
    if resp and len(resp.split()) > 1:
        # resp = binascii.hexlify(resp).decode()
        parsed = resp.split()[1].decode()
        print(parsed, "kg")
        ble_obj.send(parsed)
        sleep_ms(300)
