import akshare as ak
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 获取数据
funds = {
    "110020": ak.fund_open_fund_info_em(symbol="110020", indicator="单位净值走势"),
    "002611": ak.fund_open_fund_info_em(symbol="002611", indicator="单位净值走势"),
    "003376": ak.fund_open_fund_info_em(symbol="003376", indicator="单位净值走势"),
    "070009": ak.fund_open_fund_info_em(symbol="070009", indicator="单位净值走势"),
}

# 基金代码与中文名称映射
fund_names = {
    "110020": "易方达沪深300ETF联接A",
    "002611": "博时黄金ETF联接C",
    "003376": "广发中债7-10年国开债指数A",
    "070009": "嘉实超短债债券C",
}

# 整理数据
data = pd.DataFrame()
for fund_code, fund_data in funds.items():
    fund_data = fund_data.rename(columns={"净值日期": "date", "单位净值": fund_code})  # 重命名
    fund_data["date"] = pd.to_datetime(fund_data["date"])  # 转换日期格式
    fund_data = fund_data[["date", fund_code]]  # 保留日期和单位净值
    if data.empty:
        data = fund_data
    else:
        data = pd.merge(data, fund_data, on="date", how="outer")  # 按日期对齐

data = data.sort_values("date").reset_index(drop=True)  # 按日期排序

# 找到所有基金的共同开始时间
common_start_date = data.dropna().iloc[0]["date"]

# 筛选出共同时间段的数据
data = data[data["date"] >= common_start_date]

# 归一化处理
for fund_code in funds.keys():
    data[fund_code] = data[fund_code] / data[fund_code].iloc[0]  # 将每只基金的净值除以其第一个有效值

# 绘图
plt.figure(figsize=(12, 6))
for fund_code in funds.keys():
    plt.plot(data["date"], data[fund_code], label=fund_names[fund_code])  # 使用中文名称作为图例

plt.title("基金单位净值走势（共同开始时间，归一化）", fontsize=16)
plt.xlabel("日期", fontsize=12)
plt.ylabel("归一化净值", fontsize=12)
plt.legend(fontsize=10)
plt.grid()
plt.show()
