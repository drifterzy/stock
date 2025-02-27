import pandas as pd

from indicator.daily.ATR import calculate_atr
from indicator.daily.MA import calculate_ma


fund_code = '510300'
# 获取40日均线
result_40 = calculate_ma(fund_code, ma_days=40)
# 获取100日均线
result_100 = calculate_ma(fund_code, ma_days=100)
# 获取ATR
atr_result = calculate_atr(fund_code,period=14)

# 合并40日和100日均线的结果
combined_result = pd.merge(result_40, result_100, on=["fund_code", "net_value_date", "close_value"], how="outer")
combined_result = pd.merge(combined_result, atr_result, on=["fund_code", "net_value_date", "close_value"], how="outer")

# 保存合并后的结果
combined_result.to_excel('data/MACombineATR.xlsx', index=False)