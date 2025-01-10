import pandas as pd

def clean_data(df):
    # 替换 "尚未恢复" 为 -1
    for col in ['净值恢复所需天数', '最大回撤修复时间']:
        df[col] = df[col].replace('尚未恢复', -1).astype(float)

    # 清洗条件
    conditions = [
        ~df['基金类型'].str.contains("货币|Reits|长债", case=False, na=False),
        df['股票'] <= 30,
        df['成立时间'] <= pd.Timestamp('2020-01-01'),
        df['年化收益率'] >= 0.03,
        df['近1年年化收益率'] >= 0.03,
        df['近3年年化收益率'] >= 0.03,
        df['近5年年化收益率'] >= 0.03,
        df['季度胜率'] >= 0.8,
        df['净值恢复所需天数'] < 100,
        df['最大回撤修复时间'] < 100,
        df['最大回撤'] >= -0.01,
        df['创新高天数占比'] >= 0.5
    ]

    # 应用所有条件
    for condition in conditions:
        df = df[condition]

    return df

try:
    # 读取数据
    df = pd.read_excel("../basic/data/allFundResult.xlsx", engine='openpyxl')
    print("原始数据：", df.dtypes)

    # 清洗数据
    df_cleaned = clean_data(df)
    print("清洗后的数据：")
    print(df_cleaned.head())

    # 保存结果
    df_cleaned.to_excel("./data/gushouCodeLowRisk.xlsx", index=False, engine='openpyxl')
    print("清洗后的数据已保存。")

except FileNotFoundError:
    print("文件未找到。")
except Exception as e:
    print(f"处理文件时发生错误：{e}")
