import akshare as ak

from utils.file_tool import save_dataframe_to_excel

bond_zh_us_rate_df = ak.bond_zh_us_rate(start_date="19901219")
print(bond_zh_us_rate_df)
save_dataframe_to_excel(bond_zh_us_rate_df, '国债.xlsx', '指数')