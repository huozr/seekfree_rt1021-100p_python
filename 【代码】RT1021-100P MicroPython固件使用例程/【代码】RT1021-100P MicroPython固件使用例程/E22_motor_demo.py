from machine import *

from smartcar import *
from seekfree import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)

# 实例化 MOTOR_CONTROLLER 电机驱动模块 一共四个参数 两个必填两个可选 [mode,freq,duty,invert]
# mode - 工作模式 一共四种选项 [PWM_C24_DIR_C26,PWM_C25_DIR_C27,PWM_C24_PWM_C26,PWM_C25_PWM_C27]
#        实际对应 DRV8701 双驱双电机 以及 HIP4082 双驱双电机 请确保驱动正确且信号连接正确
# freq - PWM 频率
# duty - 可选参数 初始的占空比 默认为 0 范围 0-10000
# invert - 可选参数 是否反向 默认为 0 可以通过这个参数调整电机方向极性
motor_l = MOTOR_CONTROLLER(MOTOR_CONTROLLER.PWM_C25_DIR_C27, 13000, duty = 0, invert = True)
motor_r = MOTOR_CONTROLLER(MOTOR_CONTROLLER.PWM_C24_DIR_C26, 13000, duty = 0, invert = True)

motor_dir = 1
motor_duty = 0
motor_duty_max = 1000

while True:
    time.sleep_ms(100)
    
    if motor_dir:
        motor_duty = motor_duty + 50
        if motor_duty >= motor_duty_max:
            motor_dir = 0
    else:
        motor_duty = motor_duty - 50
        if motor_duty <= -motor_duty_max:
            motor_dir = 1
    
    led1.value(motor_duty < 0)
    # duty 接口更新占空比 范围 0-10000
    motor_l.duty(motor_duty)
    motor_r.duty(motor_duty)
    
    gc.collect()

