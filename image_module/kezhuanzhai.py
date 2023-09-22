import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd

def plot_kezhuanzhai():
    # 设置编码格式，防止中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = ak.bond_cb_index_jsl()
    # 将 'price_dt' 列转换为日期时间类型
    df['price_dt'] = pd.to_datetime(df['price_dt'])
    start_date = pd.to_datetime('2021-12-29')
    df = df[df['price_dt'] >= start_date]
    df.set_index('price_dt', inplace=True)

    # 计算 price1 和 price2 的归一化值
    price1_normalized = df['price'] / df['price'].iloc[0]
    price2_normalized = df['idx_price'] / df['idx_price'].iloc[0]

    # 使用 matplotlib 绘制图表
    plt.figure(figsize=(10, 6))  # 设置图表的大小
    plt.plot(df.index, price1_normalized, label='转债等权')  # 绘制归一化后的 price1 数据
    plt.plot(df.index, price2_normalized, label='沪深300')  # 绘制归一化后的 price2 数据

    # 添加标签和图例
    plt.xlabel('Time')
    plt.ylabel('Normalized Price')
    plt.title('转债等权vs沪深300')
    plt.legend()
    # 添加起始和结束日期标注
    start_date_label = df.index[0].strftime('%Y-%m-%d')
    end_date_label = df.index[-1].strftime('%Y-%m-%d')
    plt.annotate(f'Start: {start_date_label}', (df.index[0], price1_normalized.iloc[0]), xytext=(10, 20),
                 textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    plt.annotate(f'End: {end_date_label}', (df.index[-1], price1_normalized.iloc[-1]), xytext=(-90, -20),
                 textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    # 显示图表
    plt.grid(True)
    # 保存图表为临时文件
    chart_tmp = 'chart_kezhuanzhai_20211229.png'
    plt.savefig(chart_tmp)
    plt.close()
    return chart_tmp

plot_kezhuanzhai()