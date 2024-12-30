import pandas as pd

# 设置文件路径（相对路径）
file_path = "../basic/data/allFundHoldings.csv"

# 读取CSV文件
try:
    df = pd.read_csv(file_path)

    # 数据清洗：
    # 1. 去掉基金简称中带有 "后端" 的行
    df = df[~df['基金简称'].str.contains("后端", na=False)]

    # 2. 去掉基金类型中包含 "货币"、"Reits"、"长债" 的行
    df = df[~df['基金类型'].str.contains("货币|Reits|长债", case=False, na=False)]

    # 3. 去掉股票比率高于30的行
    df = df[df['股票'] <= 30]

    # 输出清洗后的数据
    print("清洗后的数据：")
    print(df)

    # 如果需要保存清洗后的结果
    output_path = "./data/gushouCode.csv"
    df.to_csv(output_path, index=False)
    print(f"清洗后的数据已保存到: {output_path}")

except FileNotFoundError:
    print(f"文件未找到：{file_path}")
except Exception as e:
    print(f"处理文件时发生错误：{e}")
