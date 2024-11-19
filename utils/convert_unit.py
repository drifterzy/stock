import pandas as pd

# 读取 CSV 文件
file_path = '/Users/leo/Documents/project/stock/basic/data/allFundBasicData.csv'
data = pd.read_csv(file_path, encoding='utf-8')

# 定义一个函数将规模统一转换为亿
def convert_to_billion(scale):
    if pd.isna(scale):  # 忽略空值
        return scale
    scale_str = str(scale).strip()
    if scale_str.endswith('万'):
        # 去掉 "万" 并除以 10000 转化为亿
        return float(scale_str[:-1]) / 10000
    elif scale_str.endswith('亿'):
        # 去掉 "亿" 转化为浮点数
        return float(scale_str[:-1])
    else:
        # 没有后缀的数字直接返回
        return float(scale_str)

# 应用转换函数
data['最新规模'] = data['最新规模'].apply(convert_to_billion)

# 保存结果到新文件
output_path = '/Users/leo/Documents/project/stock/basic/data/allFundBasicData_cleaned.csv'
data.to_csv(output_path, index=False, encoding='utf-8')

print(f"处理完成，结果保存至：{output_path}")
