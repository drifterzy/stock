import os
import pandas as pd

def save_dataframe_to_excel(dataframe, output_file, subdirectory=None):
    """
    将 DataFrame 保存为 Excel 文件。

    参数:
        dataframe: 要保存的 DataFrame。
        output_file: 输出的 Excel 文件名。
        subdirectory: 子目录名，如果有子目录的话。

    返回:
        无返回值。
    """
    # 获取当前脚本文件所在的目录路径
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建输出文件的完整路径
    output_dir = os.path.join(script_dir, '..', 'data', subdirectory) if subdirectory else os.path.join(script_dir, '..', 'data')
    output_path = os.path.join(output_dir, output_file)

    try:
        dataframe.to_excel(output_path, index=False)
        print(f"DataFrame已保存到 {output_path}")
    except AttributeError as e:
        print("发生错误：", e)