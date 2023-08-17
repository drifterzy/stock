import akshare as ak

from utils.file_tool import save_dataframe_to_excel

index_value_name_funddb_df = ak.index_value_name_funddb()
print(index_value_name_funddb_df)

# 调用函数保存 DataFrame 到 Excel 文件
save_dataframe_to_excel(index_value_name_funddb_df, '指数估值20230817.xlsx', '指数')