from machine import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)
# 学习板上 C21 对应霍尔停车检测接口
hall = Pin('C21' , Pin.IN , pull = Pin.PULL_UP_47K, value = True)

hall_count = 0

# 定义一个回调函数 必须有一个参数用于传递实例本身
def hall_handler(x):
    global hall_count
    hall_count = hall_count + 1
    print("hall_count ={:>6d}, hall_state ={:>6d}".format(hall_count, x.value()))

# 配置 Pin 的中断 也就是外部中断 EXTI
# 由于选择的是下降沿触发 因此回调函数中的状态一般是 0 如果改成上升沿则是 1
hall.irq(hall_handler, Pin.IRQ_FALLING, False) # IRQ_RISING IRQ_FALLING

while True:
    time.sleep_ms(1000)
    led1.toggle()
    gc.collect()
