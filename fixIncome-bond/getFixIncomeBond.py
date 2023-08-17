import akshare as ak
import os
import pandas as pd

# 获取当前脚本文件所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输出文件的完整路径
output_dir = os.path.join(script_dir, '..', 'data')  # 回退到上级目录，然后进入"data"目录
output_file = '固收+基金列表.xlsx'  # 输出文件名
output_path = os.path.join(output_dir, output_file)

# 获取基金代码列表
fund_name_em_df = ak.fund_name_em()
fund_symbols = fund_name_em_df['基金代码'].tolist()

# 定义要遍历的年份列表
years = ["2021", "2022", "2023"]

# 创建一个空的 DataFrame 用于保存结果
result_df = pd.DataFrame(columns=["基金代码", "基金简称", "基金类型"] + years)

# 遍历基金代码、年份以及基金信息
for index, row in fund_name_em_df.iterrows():
    symbol = row['基金代码']
    fund_name = row['基金简称']
    fund_type = row['基金类型']

    # 创建一个字典来存储每年的持仓权益中枢
    equity_center_dict = {"基金代码": symbol, "基金简称": fund_name, "基金类型": fund_type}

    for year in years:
        try:
            # 使用 ak.fund_portfolio_hold_em() 获取基金持仓信息的 DataFrame
            fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol=symbol, date=year)

            # 检查数据是否存在，如果不存在则使用 NaN
            if fund_portfolio_hold_em_df.empty:
                average_equity_center = float("nan")
            else:
                # 使用 groupby() 和 sum() 计算每个季度的净值之和
                quarterly_net_value_sums = fund_portfolio_hold_em_df.groupby('季度')['占净值比例'].sum()

                # 计算持仓权益中枢的均值
                average_equity_center = quarterly_net_value_sums.mean()

            # 将持仓权益中枢的均值添加到字典中
            equity_center_dict[year] = average_equity_center
        except Exception as e:
            print(f"捕获到异常：{e}",symbol,year)
            continue

    # 将当前基金的信息添加到结果 DataFrame
    result_df = result_df.append(equity_center_dict, ignore_index=True)


# 打印结果 DataFrame
# print(result_df)
try:
    result_df.to_excel(output_path, index=False)
    print(f"DataFrame已保存到 {output_path}")
except AttributeError as e:
    print("发生错误：", e)