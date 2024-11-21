import akshare as ak
import pandas as pd
import time

# 获取所有基金的基本信息
fund_name_em_df = ak.fund_name_em()
fund_list = fund_name_em_df[['基金代码', '基金简称', '基金类型']]
fund_list.to_csv("./data/allFundCode.csv", index=False, encoding="utf-8-sig")
# 创建一个空的 DataFrame 来存储结果
fund_data = pd.DataFrame(columns=['基金代码', '基金简称', '基金类型', '成立时间', '最新规模', '评级机构', '基金评级'])

# 遍历每个基金代码，获取其最新规模
for index, row in fund_list.iterrows():
    # if row['基金代码']=='000002':
    #     print("here")
    try:
        fund_info_df = ak.fund_individual_basic_info_xq(symbol=row['基金代码'])
        if not fund_info_df.empty:
            start_date = fund_info_df[fund_info_df['item'] == '成立时间']['value'].values[0]
            latest_scale = fund_info_df[fund_info_df['item'] == '最新规模']['value'].values[0]
            rate_company = fund_info_df[fund_info_df['item'] == '评级机构']['value'].values[0]
            rate_level = fund_info_df[fund_info_df['item'] == '基金评级']['value'].values[0]
            new_row = pd.DataFrame({
                '基金代码': [row['基金代码']],
                '基金简称': [row['基金简称']],
                '基金类型': [row['基金类型']],
                '成立时间': [start_date],
                '最新规模': [latest_scale],
                '评级机构': [rate_company],
                '基金评级': [rate_level]
            })
            fund_data = pd.concat([fund_data, new_row], ignore_index=True)
        else:
            print(f"基金 {row['基金代码']} 的数据不可用")
        time.sleep(1)  # 添加延迟以防止请求过于频繁
    except Exception as e:
        new_row = pd.DataFrame({
            '基金代码': [row['基金代码']],
            '基金简称': [row['基金简称']],
            '基金类型': [row['基金类型']],
            '成立时间': '',
            '最新规模': '',
            '评级机构': '',
            '基金评级': ''
        })
        fund_data = pd.concat([fund_data, new_row], ignore_index=True)
        print(f"获取基金 {row['基金代码']} 信息时出错: {e}")

# 将结果保存为 CSV 文件
fund_data.to_csv("./data/allFundBasicData.csv", index=False, encoding="utf-8-sig")
print("基金数据已保存至 fund_data2.csv")
