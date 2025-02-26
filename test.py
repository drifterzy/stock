import akshare as ak
import pandas as pd
# fund_etf_fund_daily_em = ak.fund_etf_fund_daily_em()
# fund_etf_fund_daily_em.to_excel('etf_basic.xlsx', index=False)
# print(fund_etf_fund_daily_em)


# fund_etf_fund_info_em_df = ak.fund_etf_fund_info_em(fund="510300", start_date="20000101", end_date="20500101")
# fund_etf_fund_info_em_df.to_excel('510300.xlsx', index=False)
# print(fund_etf_fund_info_em_df)

# fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()
# fund_open_fund_daily_em_df.to_excel('test.xlsx', index=False)
# print(fund_open_fund_daily_em_df)

# Set pandas display options
# pd.set_option('display.max_columns', None)  # No limit on the number of columns
# pd.set_option('display.max_rows', None)     # No limit on the number of rows
# pd.set_option('display.width', None)        # No limit on the width
# pd.set_option('display.max_colwidth', None) # No limit on column width
# testdf = ak.fund_etf_fund_daily_em()
# print(testdf.head(5))

fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol="510300", period="daily", start_date="20000101", end_date="20230201", adjust="")
print(fund_etf_hist_em_df)