import pandas as pd

# 输入和输出文件路径
input_file_path = "../basic/data/allFundResult.xlsx"
output_file_path = "./data/gushouCode.xlsx"

try:
    # 读取 Excel 文件（需指定 openpyxl 引擎）
    df = pd.read_excel(input_file_path, engine='openpyxl')

    # 数据清洗过程
    df = df[~df['基金类型'].str.contains("货币|Reits|长债", case=False, na=False)]
    df = df[df['股票'] <= 30]
    df = df[df['成立时间'] <= '2020-01-01 00:00:00']
    df = df[df['年化收益率'] >= 0.03]
    df = df[df['近5年年化收益率'] >= 0.03]
    df = df[df['季度胜率'] >= 0.8]
    df = df[~df['净值恢复所需天数'].str.contains("尚未恢复", case=False, na=False)]

    # 最大回撤小于0.01，创新高大于0.5

    # 输出清洗后的数据
    print("清洗后的数据：")
    print(df.head())  # 仅打印前几行，避免数据过多时输出混乱

    # 保存清洗后的数据到 Excel 文件
    df.to_excel(output_file_path, index=False, engine='openpyxl')
    print(f"清洗后的数据已保存到: {output_file_path}")

except FileNotFoundError:
    print(f"文件未找到：{input_file_path}")
except pd.errors.EmptyDataError:
    print("文件是空的，请检查文件内容。")
except KeyError as e:
    print(f"列缺失错误：{e}，请检查文件中是否存在所需列名。")
except Exception as e:
    print(f"处理文件时发生未知错误：{e}")
