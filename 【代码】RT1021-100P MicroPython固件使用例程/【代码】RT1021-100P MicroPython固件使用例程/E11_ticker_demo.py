from smartcar import *

import time

# 开发板上的 C19 是拨码开关
end_switch = Pin('C19', Pin.IN, pull=Pin.PULL_UP_47K, value = True)

ticker_flag = False
ticker_count = 0

# 定义一个回调函数
def time_pit_handler(time):
    global ticker_flag
    ticker_flag = True

# 实例化 PIT ticker 模块 参数为编号 [0-3] 最多四个
pit1 = ticker(1)
# 关联 Python 回调函数
pit1.callback(time_pit_handler)
# 启动 ticker 实例 参数是触发周期 单位是毫秒
pit1.start(100)

# 需要注意的是 ticker 是底层驱动的 这导致 Thonny 的 Stop 命令在这个固件版本中无法停止它
# 因此一旦运行了使用了 ticker 模块的程序 要么通过复位核心板重新连接 Thonny
# 或者像本示例一样 使用一个 IO 控制停止 Ticker 后再使用 Stop/Restart backend 按钮

while True:
    if (ticker_flag):
        ticker_flag = False
        ticker_count = ticker_count + 1
        print("Ticker trigger {:>6d}.".format(ticker_count))
    if end_switch.value() == 0:
        pit1.stop()
        break
