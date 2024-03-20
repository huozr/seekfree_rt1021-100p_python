from machine import *

from smartcar import *
from seekfree import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)
# 开发板上的 C19 是拨码开关
end_switch = Pin('C19', Pin.IN, pull=Pin.PULL_UP_47K, value = True)

# 实例化 KEY_HANDLER 模块 参数是按键扫描周期
# 扫描周期根据实际 ticker 周期或者延时周期来确定
# 请务必确保扫描周期是正确的 否则按键触发可能会有问题
key = KEY_HANDLER(10)

ticker_flag = False
ticker_count = 0
runtime_count = 0

# 定义一个回调函数
def time_pit_handler(time):
    global ticker_flag
    global ticker_count
    ticker_flag = True
    ticker_count = (ticker_count + 1) if (ticker_count < 100) else (1)

# 实例化 PIT ticker 模块 参数为编号 [0-3] 最多四个
pit1 = ticker(1)
# 关联采集接口 最少一个 最多八个
# 可关联 smartcar 的 ADC_Group_x 与 encoder_x
# 可关联 seekfree 的  IMU660RA, IMU963RA, KEY_HANDLER 和 TSL1401
pit1.capture_list(key)
# 关联 Python 回调函数
pit1.callback(time_pit_handler)
# 启动 ticker 实例 参数是触发周期 单位是毫秒
pit1.start(10)

# 需要注意的是 ticker 是底层驱动的 这导致 Thonny 的 Stop 命令在这个固件版本中无法停止它
# 因此一旦运行了使用了 ticker 模块的程序 要么通过复位核心板重新连接 Thonny
# 或者像本示例一样 使用一个 IO 控制停止 Ticker 后再使用 Stop/Restart backend 按钮

while True:
    if (ticker_flag):
        # 通过 capture 接口更新数据 但在这个例程中被 ticker 模块接管了
        # key.capture()
        # 通过 get 接口读取数据
        key_data = key.get()
        # 按键数据为三个状态 0-无动作 1-短按 2-长按
        if key_data[0]:
            print("key1 = {:>6d}.".format(key_data[0]))
            key.clear(1)
        if key_data[1]:
            print("key2 = {:>6d}.".format(key_data[1]))
            key.clear(2)
        if key_data[2]:
            print("key3 = {:>6d}.".format(key_data[2]))
            key.clear(3)
        if key_data[3]:
            print("key4 = {:>6d}.".format(key_data[3]))
            key.clear(4)
        if (ticker_count == 100):
            led1.toggle()
        ticker_flag = False
    if end_switch.value() == 0:
        pit1.stop()
        break
    
    gc.collect()
