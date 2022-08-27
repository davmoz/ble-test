from machine import Pin, Timer
from time import sleep_ms
import ubluetooth
from esp32 import raw_temperature
import _thread
import struct

class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)

        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

        self.client_connected = False

        self.value = 0

    def connected(self):
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
            self.client_connected = True
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
            self.client_connected = False


        elif event == 3:
            '''New message received'''
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)

    def register(self):

        HR_UUID = ubluetooth.UUID(0x180D)
        HR_CHAR = (ubluetooth.UUID(0x2A37), ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,)
        HR_SERVICE = (HR_UUID, (HR_CHAR,),)

        SERVICES = (HR_SERVICE,)
        # ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)
        print(self.ble.gatts_register_services(SERVICES))
        ((self.hr,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        if self.client_connected:
            payload = struct.pack('<f', float(data))
            self.ble.gatts_notify(0, self.hr, payload + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
