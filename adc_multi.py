import pinesp32
import time
import machine

# c++ https://github.com/waspinator/CD74HC4067
print("import adc_multi.py")

_g_channel_truth_table = [
    # s0, s1, s2, s3     channel
    [0,  0,  0,  0],  # 0
    [1,  0,  0,  0],  # 1
    [0,  1,  0,  0],  # 2
    [1,  1,  0,  0],  # 3
    [0,  0,  1,  0],  # 4
    [1,  0,  1,  0],  # 5
    [0,  1,  1,  0],  # 6
    [1,  1,  1,  0],  # 7
    [0,  0,  0,  1],  # 8
    [1,  0,  0,  1],  # 9
    [0,  1,  0,  1],  # 10
    [1,  1,  0,  1],  # 11
    [0,  0,  1,  1],  # 12
    [1,  0,  1,  1],  # 13
    [0,  1,  1,  1],  # 14
    [1,  1,  1,  1]   # 15
]

_S0 = machine.Pin(pinesp32.S0, machine.Pin.OUT)
_S1 = machine.Pin(pinesp32.S1, machine.Pin.OUT)
_S2 = machine.Pin(pinesp32.S2, machine.Pin.OUT)
_S3 = machine.Pin(pinesp32.S3, machine.Pin.OUT)
_ADC_MULTI = machine.ADC(machine.Pin(pinesp32.ADC_MULTI, machine.Pin.IN))

# adjust to arduino
# _ADC_MULTI.width(machine.ADC.WIDTH_10BIT) # output bit size
_ADC_MULTI.atten(machine.ADC.ATTN_11DB)  # adjusts to input voltage


def set_channel(channel: int):
    """set channel of the ADC multiplexer"""
    _S0.value(_g_channel_truth_table[channel][0])
    _S1.value(_g_channel_truth_table[channel][1])
    _S2.value(_g_channel_truth_table[channel][2])
    _S3.value(_g_channel_truth_table[channel][3])
    time.sleep_us(1)


def read_raw():
    """read raw value with ADC"""
    return _ADC_MULTI.read()
