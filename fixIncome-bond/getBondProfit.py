import pandas as pd
import os
import akshare as ak
from datetime import datetime

# 获取当前脚本文件所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输出文件的完整路径
input_dir = os.path.join(script_dir, '..', 'data\固收')
output_dir = os.path.join(script_dir, '..', 'data\固收')  # 回退到上级目录，然后进入"data"目录
input_file = '固收+基金列表3.xlsx'  # 输出文件名
input_path = os.path.join(input_dir, input_file)
output_file = '固收+基金收益.xlsx'  # 输出文件名
output_path = os.path.join(output_dir, output_file)


# 计算每年的收益率
def calculate_annual_return(data):
    if len(data) == 0:
        return 0.0

    first_value = data.iloc[0]['单位净值']
    last_value = data.iloc[-1]['单位净值']
    return_rate = (last_value - first_value) / first_value * 100
    return return_rate


# 基金历史数据-单位净值走势
def get_fund_returns(fund_code):
    fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund=fund_code, indicator="单位净值走势")

    # 将净值日期转换为日期类型
    fund_open_fund_info_em_df['净值日期'] = pd.to_datetime(fund_open_fund_info_em_df['净值日期'])

    # 提取 2021、2022 和 2023 年的数据
    data_2021 = fund_open_fund_info_em_df[(fund_open_fund_info_em_df['净值日期'].dt.year == 2021)]
    data_2022 = fund_open_fund_info_em_df[(fund_open_fund_info_em_df['净值日期'].dt.year == 2022)]
    data_2023 = fund_open_fund_info_em_df[(fund_open_fund_info_em_df['净值日期'].dt.year == 2023)]

    return (
        calculate_annual_return(data_2021),
        calculate_annual_return(data_2022),
        calculate_annual_return(data_2023)
    )


df = pd.read_excel(input_path, dtype={'基金代码': str})

# 创建一个空的DataFrame用于保存收益率数据
returns_df = pd.DataFrame(columns=['基金代码', '2021收益率', '2022收益率', '2023收益率'])

# 遍历数据框并获取基金代码
for index, row in df.iterrows():
    fund_code = row['基金代码']
    print(f'处理基金代码: {fund_code}')

    # 获取收益率
    return_2021, return_2022, return_2023 = get_fund_returns(fund_code)

    # 将基金代码和收益率添加到 returns_df
    returns_df = returns_df.append(
        {'基金代码': fund_code, '2021收益率': return_2021, '2022收益率': return_2022, '2023收益率': return_2023}, ignore_index=True)

# 将收益率数据合并到原始数据框 df
merged_df = pd.merge(df, returns_df, on='基金代码', how='left')

# 存储到一个Excel文件
merged_df.to_excel(output_path, index=False)
print(f'Saved {output_path}')