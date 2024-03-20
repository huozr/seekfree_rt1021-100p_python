from machine import *

from smartcar import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)
# 开发板上的 C19 是拨码开关
end_switch = Pin('C19', Pin.IN, pull=Pin.PULL_UP_47K, value = True)

# 实例化一个 ADC_Group 模块
# 参数代表它对应 MCU 的哪个 ADC 模块
adc_group = ADC_Group(1)
# 将四个通道添加进来
adc_group.addch('B14')
adc_group.addch('B15')
adc_group.addch('B26')
adc_group.addch('B27')

ticker_flag = False
ticker_count = 0

# 定义一个回调函数
def time_pit_handler(time):
    global ticker_flag
    global ticker_count
    ticker_flag = True
    ticker_count = (ticker_count + 1) if (ticker_count < 100) else (1)

# 实例化 PIT ticker 模块 参数为编号 [0-3] 最多四个
pit1 = ticker(1)
# 关联采集接口 最少一个 最多八个 (imu, ccd, key...)
# 可关联 smartcar 的 ADC_Group_x 与 encoder_x
# 可关联 seekfree 的  IMU660RA, IMU963RA, KEY_HANDLER 和 TSL1401
pit1.capture_list(adc_group)
# 关联 Python 回调函数
pit1.callback(time_pit_handler)
# 启动 ticker 实例 参数是触发周期 单位是毫秒
pit1.start(10)

# 需要注意的是 ticker 是底层驱动的 这导致 Thonny 的 Stop 命令在这个固件版本中无法停止它
# 因此一旦运行了使用了 ticker 模块的程序 要么通过复位核心板重新连接 Thonny
# 或者像本示例一样 使用一个 IO 控制停止 Ticker 后再使用 Stop/Restart backend 按钮

while True:
    if (ticker_flag and ticker_count == 100):
        led1.toggle()
        # 通过 capture 接口触发一次转换 无参数
        # capture 接口可以被 Ticker 接管
        # adc_group.capture()
        # 通过 get 接口获取数据 数据返回范围是 0-4095
        adc_data = adc_group.get()
        print("adc={:>6d},{:>6d},{:>6d},{:>6d}.\r\n".format(
            adc_data[0],
            adc_data[1],
            adc_data[2],
            adc_data[3]))
        ticker_flag = False
    if end_switch.value() == 0:
        pit1.stop()
        break
    
    gc.collect()
