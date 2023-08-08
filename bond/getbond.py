import akshare as ak

file_path = r'D:\study\stock\基金实时数据.csv'


fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()


fund_open_fund_daily_em_df.to_csv(file_path, index=False)
print(f"DataFrame已保存到 {file_path}")

