import akshare as ak
df = ak.fund_open_fund_info_em(symbol="008569", indicator="累计净值走势")
df.to_csv("./basic/data/008569.csv", encoding="utf-8-sig", index=False)
print(df)