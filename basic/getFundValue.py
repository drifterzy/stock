import akshare as ak
import pandas as pd
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="000005", indicator="累计净值走势")
# print(fund_open_fund_info_em_df)
#
# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="013964", indicator="单位净值走势")
# print(fund_open_fund_info_em_df)


fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()
fund_name_em_df = ak.fund_name_em()


# 提取两者不同的基金代码
open_fund_codes = set(fund_open_fund_daily_em_df["基金代码"])
name_fund_codes = set(fund_name_em_df["基金代码"])

# 只在 fund_open_fund_daily_em_df 中存在的基金代码
only_in_open_fund = open_fund_codes - name_fund_codes

# 只在 fund_name_em_df 中存在的基金代码
only_in_name_fund = name_fund_codes - open_fund_codes

# 将结果转换为 DataFrame
only_in_open_fund_df = pd.DataFrame({"基金代码": list(only_in_open_fund)})
only_in_name_fund_df = pd.DataFrame({"基金代码": list(only_in_name_fund)})

# 保存为 CSV 文件
only_in_open_fund_df.to_csv("./data/only_in_open_fund.csv", index=False, encoding="utf-8")
only_in_name_fund_df.to_csv("./data/only_in_name_fund.csv", index=False, encoding="utf-8")

print("差异基金代码已保存为 CSV 文件！")