from machine import *

import time
import gc

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)

pwm_servo_hz = 300

# 定义一个角度与占空比换算的函数 传入参数为 PWM 的频率和目标角度
def duty_angle (freq, angle):
    return (65535.0 / (1000.0 / freq) * (0.5 + angle / 90.0))

# 初始角度 90 度 也就是舵机中值角度
angle = 90.0
# 舵机动作方向
dir = 1
# 获取舵机中值角度对应占空比
duty = int(duty_angle(pwm_servo_hz, angle))
# 学习板上舵机接口为 C20
pwm_servo = PWM("C20", pwm_servo_hz, duty_u16 = duty)

while True:
    time.sleep_ms(50)
    # 往复计算舵机角度
    if dir:
        angle = angle + 0.1
        if angle >= 95.0:
            dir = 0
            led1.toggle()
    else:
        angle = angle - 0.1
        if angle <= 85.0:
            dir = 1
            led1.toggle()
    # 获取舵机角度对应占空比
    duty = int(duty_angle(pwm_servo_hz, angle))
    # 设置更新 PWM 输出后可以看到舵机动作
    pwm_servo.duty_u16(duty)
    
    gc.collect()
