import akshare as ak
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from utils.plot_imag import plot_stock_price_trend_multi_same_scale, plot_stock_price_trend_multi, \
    plot_stock_price_trend

# df = ak.fund_etf_hist_em(symbol="510300", period="daily", start_date="20120602", end_date="20230818", adjust="hfq")
df2 = ak.fund_etf_hist_em(symbol="510300", period="daily", start_date="20120602", end_date="20230818", adjust="qfq")
# df3 = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20120602", end_date="20230818")
df4 = stock_a_all_pb_df = ak.stock_a_all_pb()

# plot_stock_price_trend(df)
# plot_stock_price_trend(df2)
# plot_stock_price_trend_multi_same_scale(df,df2)
plot_stock_price_trend_multi(df2,df4,'date','middlePB')