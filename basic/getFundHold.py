import pandas as pd
import akshare as ak
import time
# 参数
date = '20241216'

# 读取原始 CSV 文件
input_csv = "./data/allFundBasicData_cleaned.csv"  # 替换为你的输入文件名
fund_data = pd.read_csv(input_csv)

# 创建一个空的 DataFrame，用于存储所有基金的结果
all_fund_results = pd.DataFrame()

# 固定的列名
fixed_columns = ['股票', '债券', '现金', '其他']

# 遍历基金代码
for index, row in fund_data.iterrows():
    fund_code = row['基金代码']

    # 跳过空值或无效基金代码
    if pd.isna(fund_code):
        continue

    # 确保基金代码是字符串格式
    fund_code = str(fund_code).zfill(6)
    # 读取当前基金的其他属性
    fund_name = row['基金简称']
    fund_type = row['基金类型']
    established_date = row['成立时间']
    latest_scale = row['最新规模']

    try:
        # 获取数据
        fund_individual_detail_hold_xq_df = ak.fund_individual_detail_hold_xq(symbol=fund_code, date=date)

        # 转置数据
        transposed_df = fund_individual_detail_hold_xq_df.set_index("资产类型").T

        # 添加基金代码列
        transposed_df["基金代码"] = fund_code
        transposed_df["基金简称"] = fund_name
        transposed_df["基金类型"] = fund_type
        transposed_df["成立时间"] = established_date
        transposed_df["最新规模"] = latest_scale

        # 创建一个包含固定列名的列字典，初始化为0
        for col in fixed_columns:
            transposed_df[col] = transposed_df.get(col, 0)

        # 填充无值的列为0
        for col in fixed_columns:
            if col not in transposed_df.columns:
                transposed_df[col] = 0

        # 保证列的顺序固定
        column_order = ['基金代码', '基金简称', '基金类型', '成立时间', '最新规模'] + fixed_columns
        transposed_df = transposed_df[column_order]

        # 将结果追加到总结果中
        all_fund_results = pd.concat([all_fund_results, transposed_df], ignore_index=True)
        time.sleep(1)  # 添加延迟以防止请求过于频繁
    except Exception as e:
        # 异常处理：生成一个空行并添加到 DataFrame 中
        new_row = pd.DataFrame({
            '基金代码': [fund_code],
            '基金简称': [fund_name],
            '基金类型': [fund_type],
            '成立时间': [established_date],
            '最新规模': [latest_scale],
            '股票': '',
            '债券': '',
            '现金': '',
            '其他': ''
        })
        all_fund_results = pd.concat([all_fund_results, new_row], ignore_index=True)
        print(f"获取基金 {row['基金代码']} 信息时出错: {e}")

# 输出到最终的 CSV 文件
all_fund_results.to_csv("./data/allFundHoldings.csv", encoding="utf-8-sig", index=False)
print("基金数据已保存至 allFundHoldings.csv")
