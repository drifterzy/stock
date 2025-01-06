import akshare as ak

df = ak.fund_name_em()
# 去除基金代码中含有“后端”两个字的行
df_filtered = df[~df['基金简称'].str.contains('后端')]
print(df)