import akshare as ak

# 设置中文字体
from utils.file_tool import save_dataframe_to_excel

index_zh_a_hist_df = ak.index_zh_a_hist(symbol="399300", period="daily", start_date="20230101", end_date="20230817")
print(index_zh_a_hist_df)

# 调用函数保存 DataFrame 到 Excel 文件
save_dataframe_to_excel(index_zh_a_hist_df, '沪深300_20230817.xlsx', '指数')