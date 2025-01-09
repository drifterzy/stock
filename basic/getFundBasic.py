import akshare as ak
import pandas as pd
import time

# 定义常量
ALL_FUNDS_FILE = "./data/allFundCode.xlsx"
BASIC_DATA_FILE = "./data/allFundBasicData.xlsx"
CLEANED_DATA_FILE = "./data/allFundBasicData_cleaned.xlsx"
DATE = '20250108'

# 获取所有基金的基本信息并保存到 Excel 文件
def fetch_all_fund_info():
    fund_name_em_df = ak.fund_name_em()
    fund_list = fund_name_em_df[['基金代码', '基金简称', '基金类型']]
    fund_list = fund_list[~fund_list['基金简称'].str.contains('后端')]
    return fund_list

# 获取单个基金的详细信息
def fetch_fund_details(fund_code, fund_name, fund_type):
    try:
        fund_info_df = ak.fund_individual_basic_info_xq(symbol=fund_code)
        if not fund_info_df.empty:
            start_date = fund_info_df[fund_info_df['item'] == '成立时间']['value'].values[0]
            latest_scale = fund_info_df[fund_info_df['item'] == '最新规模']['value'].values[0]
            return {
                '基金代码': fund_code,
                '基金简称': fund_name,
                '基金类型': fund_type,
                '成立时间': start_date,
                '最新规模': latest_scale
            }
    except Exception as e:
        print(f"获取 {fund_code} 的规模信息时出错: {e}")
    return {
        '基金代码': fund_code,
        '基金简称': fund_name,
        '基金类型': fund_type,
        '成立时间': '',
        '最新规模': ''
    }

# 获取基金持仓数据
def fetch_fund_holdings(fund_code):
    try:
        fund_holdings = ak.fund_individual_detail_hold_xq(symbol=str(fund_code).zfill(6), date=DATE)
        transposed_df = fund_holdings.set_index("资产类型").T
        FIXED_COLUMNS = ['股票', '债券', '现金', '其他']
        for col in FIXED_COLUMNS:
            transposed_df[col] = transposed_df.get(col, 0)
        total = transposed_df.loc['仓位占比', '股票']+transposed_df.loc['仓位占比', '债券']+transposed_df.loc['仓位占比', '现金']+transposed_df.loc['仓位占比', '其他']
        return {
            '股票': transposed_df.loc['仓位占比', '股票'],
            '债券': transposed_df.loc['仓位占比', '债券'],
            '现金': transposed_df.loc['仓位占比', '现金'],
            '其他': transposed_df.loc['仓位占比', '其他'],
            '总和': total
        }

    except Exception as e:
        print(f"获取 {fund_code} 的持仓信息时出错: {e}")
    return {
            '股票': '',
            '债券': '',
            '现金': '',
            '其他': '',
            '总和': ''
    }

# 遍历基金列表并获取详细信息
def fetch_all_fund_details(fund_list):
    fund_data = pd.DataFrame(columns=['基金代码', '基金简称', '基金类型', '成立时间', '最新规模', '股票', '债券', '现金', '其他'])
    for _, row in fund_list.iterrows():
        try:
            print(f"处理 {row['基金代码']} ")
            fund_details = fetch_fund_details(row['基金代码'], row['基金简称'], row['基金类型'])
            fund_holdings = fetch_fund_holdings(row['基金代码'])
            # 确保两个 DataFrame 是可以拼接的
            details_df = pd.DataFrame([fund_details])
            holdings_df = pd.DataFrame([fund_holdings])
            # 合并基金详细信息和持仓信息
            merged_df = pd.concat([details_df, holdings_df], axis=1)
            # 将结果追加到最终结果 DataFrame
            fund_data = pd.concat([fund_data, merged_df], ignore_index=True)
        except Exception as e:
            print(f"处理 {row['基金代码']} 时出错: {e}")
            fund_data = pd.concat([fund_data, pd.DataFrame([{
                '基金代码': row['基金代码'],
                '基金简称': row['基金简称'],
                '基金类型': row['基金类型'],
                '成立时间': '',
                '最新规模': '',
                '股票': '',
                '债券': '',
                '现金': '',
                '其他': ''
            }])], ignore_index=True)
        # time.sleep(1)  # 防止请求过于频繁
    return fund_data

# 转换规模为统一单位（亿）
def convert_to_billion(scale):
    if pd.isna(scale):
        return scale
    scale_str = str(scale).strip()
    if scale_str.endswith('万'):
        return float(scale_str[:-1]) / 10000
    elif scale_str.endswith('亿'):
        return float(scale_str[:-1])
    return float(scale_str)

# 清洗数据并保存
def clean_and_save_fund_data():
    data = pd.read_excel(BASIC_DATA_FILE)
    data['最新规模'] = data['最新规模'].apply(convert_to_billion)
    return data

# 主函数
def main():
    start_time = time.time()  # 程序开始时间
    print("开始获取基本信息...")
    fund_list = fetch_all_fund_info()
    fund_list.to_excel(ALL_FUNDS_FILE, index=False)
    print(f"基本信息已保存至：{ALL_FUNDS_FILE}")

    print("开始获取详细信息...")
    fund_data = fetch_all_fund_details(fund_list)
    fund_data.to_excel(BASIC_DATA_FILE, index=False)
    print(f"详细信息已保存至：{BASIC_DATA_FILE}")

    print("开始清洗数据...")
    cleaned_data = clean_and_save_fund_data()
    cleaned_data.to_excel(CLEANED_DATA_FILE, index=False)
    print(f"处理完成，结果保存至：{CLEANED_DATA_FILE}")
    end_time = time.time()  # 程序结束时间

    # 打印程序执行时间
    elapsed_time = end_time - start_time
    print(f"程序执行完毕，总耗时：{elapsed_time:.2f} 秒")  # 精确到小数点后2位

if __name__ == "__main__":
    main()
