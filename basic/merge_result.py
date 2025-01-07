import pandas as pd


def merge_with_existing_file(indicator_file, additional_file, output_file):
    """
    合并生成的指标文件和已有的文件。

    参数:
    indicator_file: str - 指标文件路径（生成的 CSV/Excel 文件）。
    additional_file: str - 需要合并的现有文件路径。
    output_file: str - 输出文件路径。
    """
    # 读取生成的指标文件
    if indicator_file.endswith('.xlsx'):
        indicators_df = pd.read_excel(indicator_file)
    else:
        indicators_df = pd.read_csv(indicator_file)

    # 读取现有文件
    additional_df = pd.read_csv(additional_file)

    # 确保列名一致（如必要，可调整列名）
    # additional_df.rename(columns={'基金代码': 'fund_code'}, inplace=True)

    # 合并文件，按基金代码进行外连接
    merged_df = pd.merge(indicators_df, additional_df, on='基金代码', how='left')

    # 保存合并后的文件
    if output_file.endswith('.xlsx'):
        merged_df.to_excel(output_file, index=False)
    else:
        merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"合并后的文件已保存到 {output_file}")


# 主函数
def main():
    # 假设生成的指标文件名为 'fund_performance.xlsx'
    indicator_file = './data/fund_performance.xlsx'

    # 需要合并的现有文件名为 'existing_fund_data.csv'
    additional_file = './data/allFundHoldings_combined.csv'

    # 合并后输出的文件名
    output_file = './data/merged_fund_data.xlsx'

    merge_with_existing_file(indicator_file, additional_file, output_file)


# 示例调用
if __name__ == '__main__':
    main()
