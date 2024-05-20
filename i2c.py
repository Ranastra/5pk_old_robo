import machine
import time
import pinesp32

I2C = machine.I2C(
    0,
    scl=machine.Pin(pinesp32.SCL),
    sda=machine.Pin(pinesp32.SDA)
)


def test():
    """scan for i2c devices"""
    while True:
        print("Scanning...")
        devices = I2C.scan()
        if len(devices) == 0:
            print("No I2C devices found")
        else:
            for address in devices:
                print(
                    "I2C device found at address 0x{:02X}!".format(address))
        print("Done\n")
        time.sleep(5)  # Wait 5 seconds for the next scan
