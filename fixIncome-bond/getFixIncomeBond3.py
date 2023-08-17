import pandas as pd
import os
import akshare as ak
from datetime import datetime

# 获取当前脚本文件所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建输出文件的完整路径
input_dir = os.path.join(script_dir, '..', 'data\固收')
output_dir = os.path.join(script_dir, '..', 'data\固收')  # 回退到上级目录，然后进入"data"目录
input_file = '固收+基金列表2.xlsx'  # 输出文件名
input_path = os.path.join(input_dir, input_file)
output_file = '固收+基金列表3.xlsx'  # 输出文件名
output_path = os.path.join(output_dir, output_file)

df = pd.read_excel(input_path, dtype={'基金代码': str})


# 将存在空值的单元格补为0
df.fillna(0, inplace=True)

# 仅保留同时满足2021、2022和2023年均小于30的基金数据
filtered_df = df[(df['2021'] < 30) & (df['2022'] < 30) & (df['2023'] < 30)]

# 存储到一个Excel文件
filtered_df.to_excel(output_path, index=False)
print(f'Saved {output_path}')