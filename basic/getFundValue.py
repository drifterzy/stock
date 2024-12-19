import akshare as ak

fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="013964", indicator="累计净值走势")
print(fund_open_fund_info_em_df)

fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="013964", indicator="单位净值走势")
print(fund_open_fund_info_em_df)