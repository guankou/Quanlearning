from qlib import init
from qlib.constant import REG_CN  # 从 constant 模块导入 REG_CN
from qlib.data import D
import pandas as pd

# 初始化Qlib，指定你的数据路径
init(provider_uri="/media/mu/D/ubuntu/quan_data", region=REG_CN)

# # 1. 检查交易日历（应输出非空的日期列表）
# print("交易日历示例：", D.calendar(freq="day")[:5])

# # 2. 检查股票列表（应输出部分股票代码）
# print("股票列表示例：", D.list_instruments(instruments=D.instruments("all"), as_list=True)[:5])

# # 3. 检查具体股票的特征数据（以sz300641为例）
# df = D.features(["sz300641"], ["$open", "$close"], freq="day")
# print("sz300641的开盘/收盘价数据：\n", df.head())

def get_multi_freq_data(instrument="SH600519", start_time="2010-01-01", end_time="2023-12-31"):
    # 获取日频数据（包含开盘价、收盘价、成交量）
    fields = ["$open", "$close", "$volume"]
    daily_data = D.features(
        instruments=[instrument],
        fields=fields,
        start_time=start_time,
        end_time=end_time,
        freq="day"
    )
    
    # 关键修复：将多层索引转换为时间索引（去掉instrument层，因为这里只查了一只股票）
    # 方法1：如果只查询单只股票，直接.droplevel去掉instrument索引
    daily_data = daily_data.droplevel(level=0)  # 去掉第一层（instrument）索引，仅剩datetime
    
    # 方法2：如果查询多只股票，按股票分组后重采样（通用写法）
    # daily_data = daily_data.unstack(level=0)  # 将instrument展开为列，datetime为索引
    
    # 聚合为周频数据（每周最后一个交易日）
    weekly_data = daily_data.resample("W-FRI").last()  # 周五作为周结日
    weekly_data["$volume"] = daily_data["$volume"].resample("W-FRI").sum()  # 周成交量求和
    
    # 聚合为月频数据（每月最后一个交易日）
    monthly_data = daily_data.resample("M").last()  # 月末最后一个交易日
    monthly_data["$volume"] = daily_data["$volume"].resample("M").sum()  # 月成交量求和
    
    return daily_data, weekly_data, monthly_data

# 测试：获取贵州茅台（SH600519）的多频率数据
daily, weekly, monthly = get_multi_freq_data(instrument="SH600519")
print("日K数据:\n", daily.head())
print("周K数据:\n", weekly.head())
print("月K数据:\n", monthly.head())