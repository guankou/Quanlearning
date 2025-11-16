from qlib import init
from qlib.constant import REG_CN  # 从 constant 模块导入 REG_CN
from qlib.data import D
import pandas as pd

# 初始化Qlib，指定你的数据路径
init(provider_uri="/media/mu/D/ubuntu/quan_data", region=REG_CN)

# 1. 检查交易日历（应输出非空的日期列表）
print("交易日历示例：", D.calendar(freq="day")[:5])

# 2. 检查股票列表（应输出部分股票代码）
print("股票列表示例：", D.list_instruments(instruments=D.instruments("all"), as_list=True)[:5])

# 3. 检查具体股票的特征数据（以sz300641为例）
df = D.features(["sz300641"], ["$open", "$close"], freq="day")
print("sz300641的开盘/收盘价数据：\n", df.head())