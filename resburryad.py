#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
retuenAD的功能是返回树莓派ad口的数值。
使用的时候需要放在while True里面进行配合使用。
"""

import time
import ADS1256
import RPi.GPIO as GPIO


ADC = ADS1256.ADS1256()
ADC.ADS1256_init()

def retuenAD():    
    ADC_Value = ADC.ADS1256_GetAll()
    ad1 = ADC_Value[0]*5.0/0x7fffff
    ad2 = ADC_Value[1]*5.0/0x7fffff
    ad3 = ADC_Value[2]*5.0/0x7fffff
    ad4 = ADC_Value[3]*5.0/0x7fffff
    ad5 = ADC_Value[4]*5.0/0x7fffff
    ad6 = ADC_Value[5]*5.0/0x7fffff
    ad7 = ADC_Value[6]*5.0/0x7fffff
    ad8 = ADC_Value[7]*5.0/0x7fffff
    return ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8


        
# except :
#     GPIO.cleanup()
#     print ("\r\nProgram end     ")
#     exit()
