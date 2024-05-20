########### ADC Multiplexer (CD74HC4067S)############

S0 = 4
S1 = 5
S2 = 12
S3 = 13
ADC_MULTI = 39

ADC_PT_REF_L = 0  # silver
ADC_PT_L_1 = 1
ADC_PT_L_0 = 2
ADC_PT_M = 3
ADC_PT_R_0 = 4
ADC_PT_R_1 = 5
ADC_PT_REF_R = 6  # silver
ADC_PT_RGB = 7
ADC_AE1 = 8  # External Analog Input
ADC_AE2 = 9  # External Analog Input
ADC_AE3 = 10  # External Analog Input


##################### Servos#########################

SERVO1 = 19
SERVO2 = 18
SERVO3 = 17
SERVO4 = 16

############# Motor Driver (TB6612FNG)###############

PWMA = 23
PWMB = 25

############ Shiftregister (74HC595PW)###############

SHCP = 27
STCP = 32
DS = 33

# Shiftregister IC10

SR_AIN1 = 0
SR_AIN2 = 1
SR_BIN1 = 2
SR_BIN2 = 3
SR_STBY = 4
SR_PT_WHITE = 5  # Light sensor bar white led ##HIGH - ON
SR_PT_RED = 6  # Light sensor bar red led
SR_PT_GREEN = 7  # Light sensor bar green led

# Shiftregister IC12

SR_PT_BLUE = 8  # Light sensor bar blue led
SR_LED_L_RED = 9  # LOW - ON
SR_LED_L_GREEN = 10  # status leds
SR_LED_L_BLUE = 11
SR_LED_R_RED = 12
SR_LED_R_GREEN = 13
SR_LED_R_BLUE = 14
SR_XSHT1 = 15  # TOF Select

# Shiftregister IC13

SR_XSHT2 = 16
SR_XSHT3 = 17
SR_XSHT4 = 18
SR_DE1 = 19
SR_DE2 = 20
SR_DE3 = 21  # External Digital Pins

################# Rotary Encoder#####################

ENC_A = 35
ENC_B = 34
ENC_SW = 15

################# extern Buttons#####################

T_L = 2  # Button left
T_R = 14  # Button right
T_M = 26  # Button center

##################### Battery########################

VBAT = 36

###################### I2C###########################

SDA = 21
SCL = 22
MPU6050_ADRESS = 0x68  # 0x51 in c++
OLED_ADRESS = 0x3C
TOF_ADRESS = 0x29
