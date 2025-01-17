import  akshare as ak
df = ak.fund_open_fund_daily_em()
df = df[df['基金代码'].str.contains('090010')]
print(df)