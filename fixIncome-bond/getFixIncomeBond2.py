import pandas as pd
import os
import akshare as ak
from datetime import datetime

# 获取当前脚本文件所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输出文件的完整路径
input_dir = os.path.join(script_dir, '..', 'data')
output_dir = os.path.join(script_dir, '..', 'data\固收')  # 回退到上级目录，然后进入"data"目录
input_file = '固收+基金列表.xlsx'  # 输出文件名
input_path = os.path.join(input_dir, input_file)
output_file = '固收+基金列表1.xlsx'  # 输出文件名
output_file2 = '固收+基金列表3.xlsx'  # 输出文件名
output_path = os.path.join(output_dir, output_file)
output_path2 = os.path.join(output_dir, output_file2)

# 读取Excel文件
df = pd.read_excel(input_path,dtype={'基金代码': str})

# 筛选出以C结尾的基金数据
c_ending_df = df[~df['基金简称'].str.endswith('C')]

# 筛选掉基金简称中包含"(后端)"的数据
filtered_df = c_ending_df[~c_ending_df['基金简称'].str.contains('\(后端\)')]

# 筛选掉基金简称完全相同的数据
deduplicated_df = filtered_df.drop_duplicates(subset=['基金简称'], keep=False)

# 根据基金类型筛选数据
selected_fund_types = [
    '债券型-长债',
    '混合型-灵活',
    '混合型-偏债',
    '债券型-混合债',
    '债券型-中短债',
    '混合型-平衡'
]
final_filtered_df = deduplicated_df[deduplicated_df['基金类型'].isin(selected_fund_types)]

# 存储到一个Excel文件
final_filtered_df.to_excel(output_path, index=False)
print(f'Saved {output_path}')

# 筛选出交易日期早于2021-01-01的基金数据
early_traded_funds = []

for fund_code in final_filtered_df['基金代码']:
    try:
        fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund=fund_code, indicator="单位净值走势")
        if len(fund_open_fund_info_em_df) > 1:
            first_trade_date = fund_open_fund_info_em_df.iloc[1]['净值日期']
            if first_trade_date < datetime(2021, 1, 1).date():
                print(f"基金代码 {fund_code} 的交易日期早于2021-01-01")
                early_traded_funds.append(fund_code)
    except Exception as e:
        print(f"获取基金代码 {fund_code} 的数据时出现异常：{e}")

# 筛选出交易日期早于2021-01-01的基金数据
early_traded_funds_df = final_filtered_df[final_filtered_df['基金代码'].isin(early_traded_funds)]

# 存储到一个Excel文件
early_traded_funds_df.to_excel(output_path2, index=False)
print(f'Saved {output_path2}')
