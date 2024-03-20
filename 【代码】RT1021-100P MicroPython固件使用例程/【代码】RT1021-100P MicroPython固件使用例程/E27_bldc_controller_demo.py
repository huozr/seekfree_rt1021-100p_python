from machine import *

from seekfree import *

import time
import gc

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)
key1 = Pin('D23', Pin.IN , pull = Pin.PULL_UP_47K, value = True)

# 初始 1.1ms 高电平 确保能够起转
high_level_us = 1100
# 动作方向
dir = 1
# 学习板上 BLDC 电调接口为 B26/B27
# index - 对应接口 [PWM_B26,PWM_B27]
# freq - 可选参数 PWM 频率 范围 50-300 默认 50
# highlevel_us - 可选参数 初始的高电平时长 范围 1000-2000 默认 1000
bldc1 = BLDC_CONTROLLER(BLDC_CONTROLLER.PWM_B26, freq=300, highlevel_us = 1000)
bldc2 = BLDC_CONTROLLER(BLDC_CONTROLLER.PWM_B27, freq=300, highlevel_us = 1000)

# 电调一般起转需要在 1.1ms 高电平时间比较保险
# 因为 电机各不一样 会有一些死区差异 同时安装后有负载差异

print("Wait for KEY-D23 to be pressed.\r\n")
while True:
    time.sleep_ms(100)
    led1.toggle()
    if 0 == key1.value():
        print("BLDC Controller test running.\r\n")
        print("Press KEY-D23 to suspend the program.\r\n")
        time.sleep_ms(300)
        break

while True:
    time.sleep_ms(100)
    led1.toggle()
    # 往复计算 BLDC 电调速度
    if dir:
        high_level_us = high_level_us + 5
        if high_level_us >= 1250:
            dir = 0
    else:
        high_level_us = high_level_us - 5
        if high_level_us <= 1100:
            dir = 1
    
    # 设置更新 PWM 输出后可以看到舵机动作
    bldc1.highlevel_us(high_level_us)
    bldc2.highlevel_us(high_level_us)
    
    if 0 == key1.value():
        print("Suspend.\r\n")
        print("Wait for KEY-D23 to be pressed.\r\n")
        bldc1.highlevel_us(1000)
        bldc2.highlevel_us(1000)
        time.sleep_ms(300)
        while True:
            if 0 == key1.value():
                print("BLDC Controller test running.\r\n")
                print("Press KEY-D23 to suspend the program.\r\n")
                high_level_us = 1100
                dir = 1
                time.sleep_ms(300)
                break
    
    gc.collect()
