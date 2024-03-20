from machine import *

from smartcar import *
from seekfree import *

import gc
import time

# 开发板上的 C19 是拨码开关
end_switch = Pin('C19', Pin.IN, pull=Pin.PULL_UP_47K, value = True)

# 调用 TSL1401 模块获取 CCD 实例
# 参数是采集周期 调用多少次 capture 更新一次数据
# 默认参数为 1 调整这个参数相当于调整曝光时间倍数
ccd = TSL1401(10)

# 实例化 WIRELESS_UART 模块 参数是波特率
# 无线串口模块需要自行先配对好设置好参数
wireless = WIRELESS_UART(460800)

# 发送字符串的函数
wireless.send_str("Hello World.\r\n")
time.sleep_ms(500)

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
pit1.capture_list(ccd)
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
        # ccd.capture()
        # 通过 get 接口读取数据 参数 [0,1] 对应学习板上 CCD1/2 接口
        ccd_data1 = ccd.get(0)
        ccd_data2 = ccd.get(1)
        
        # send_ccd_image 将对应编号的 CCD 数据上传到逐飞助手
        # 可选参数仅有两个 WIRELESS_UART.[CCD1_BUFFER_INDEX,CCD2_BUFFER_INDEX]
        wireless.send_ccd_image(WIRELESS_UART.CCD1_BUFFER_INDEX)
        
        ticker_flag = False
        runtime_count = runtime_count + 1
        print("runtime_count = {:>6d}.".format(runtime_count))
    
    if end_switch.value() == 0:
        pit1.stop()
        break
    
    gc.collect()
