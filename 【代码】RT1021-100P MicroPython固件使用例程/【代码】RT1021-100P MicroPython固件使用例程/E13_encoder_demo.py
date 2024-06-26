from smartcar import *

import gc
import time

# 核心板上 C4 是 LED
led1 = Pin('C4' , Pin.OUT, pull = Pin.PULL_UP_47K, value = True)
# 开发板上的 C19 是拨码开关
end_switch = Pin('C19', Pin.IN, pull=Pin.PULL_UP_47K, value = True)

# 实例化 encoder 模块
# 对应学习板的编码器接口 1/2
# 总共三个参数 两个必要参数一个可选参数 [pinA,pinB,invert]
# pinA - 编码器 A 相或 PLUS 引脚
# pinB - 编码器 B 相或 DIR 引脚
# invert - 可选参数 是否反向 可以通过这个参数调整编码器旋转方向数据极性
encoder_l = encoder("D0", "D1", True)
encoder_r = encoder("D2", "D3")

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
pit1.capture_list(encoder_l, encoder_r)
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
        # 通过 capture 接口更新数据 但在这个例程中被 ticker 模块接管了
        # encoder_l.capture()
        # encoder_r.capture()
        # 通过 get 接口读取数据
        encl_data = encoder_l.get()
        encr_data = encoder_r.get()
        print("enc ={:>6d}, {:>6d}\r\n".format(encoder_l.get(), encoder_r.get()))
        ticker_flag = False
    if end_switch.value() == 0:
        pit1.stop()
        break
    
    gc.collect()
