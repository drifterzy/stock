import akshare as ak
import pandas as pd
import time
import akshare as ak

fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="110020", indicator="累计净值走势")
print(fund_open_fund_info_em_df)