from machine import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)

# 运放对应的四个引脚都支持 ADC1 当引脚支持两个模块通道时优先分配到 ADC1 功能
adc_in1 = ADC('B14')
adc_in2 = ADC('B15')
adc_in3 = ADC('B26')
adc_in4 = ADC('B27')

while True:
    time.sleep_ms(500)
    led1.toggle()
    
    # 读取通过 read_u16 接口读取 无参数 数据返回范围是 0-65535
    print("adc={:>6d},{:>6d},{:>6d},{:>6d}.\r\n".format(
        adc_in1.read_u16(),
        adc_in2.read_u16(),
        adc_in3.read_u16(),
        adc_in4.read_u16()))
    
    gc.collect()
