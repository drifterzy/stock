import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # windwos中文显示
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

def plot_fund_net_value_curves(output_file, *fund_codes):
    # 创建一个空的 DataFrame 用于存储对齐后的数据
    aligned_data = pd.DataFrame()

    for code in fund_codes:
        code = str(code).zfill(6)
        # 获取基金累计净值数据
        fund_data = ak.fund_open_fund_info_em(symbol=str(code), indicator="累计净值走势")
        fund_data["净值日期"] = pd.to_datetime(fund_data["净值日期"])  # 转换日期格式
        fund_data = fund_data.rename(columns={"累计净值": f"基金{code}"})  # 重命名净值列
        if aligned_data.empty:
            aligned_data = fund_data
        else:
            # 按日期合并数据
            aligned_data = pd.merge(aligned_data, fund_data, on="净值日期", how="outer")

    # 对齐数据后按日期排序
    aligned_data = aligned_data.sort_values(by="净值日期").set_index("净值日期")
    # 将对齐后的数据保存到 CSV 文件
    aligned_data.to_csv(output_file, encoding="utf-8-sig")
    print(f"对齐后的数据已保存到 {output_file}")
    # 绘制累计净值曲线
    aligned_data.plot(figsize=(12, 6), title="基金累计净值曲线", grid=True)
    plt.xlabel("日期")
    plt.ylabel("累计净值")
    plt.legend(title="基金代码", loc="best")
    plt.show()


# 调用函数绘制20个基金的累计净值曲线
plot_fund_net_value_curves(
    "./data/fundAlignedData.csv",
    6966, 6965, 7456, 6824, 9617, 6829, 7582, 5838, 6434, 2920,
    7014, 9721, 6516, 7015, 6076, 6825, 9087, 10810, 8820, 9219
)
