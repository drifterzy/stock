import plotly.graph_objects as go
import pandas as pd
def plot_stock_price_trend(df, title=None):
    fig = go.Figure()

    # 添加收盘价曲线
    fig.add_trace(go.Scatter(x=df['日期'], y=df['收盘'], mode='lines', name='收盘价'))

    # 添加收盘价数据点
    fig.add_trace(go.Scatter(x=df['日期'], y=df['收盘'], mode='markers', name='收盘价数据点'))

    fig.update_xaxes(tickformat='%Y-%m-%d', nticks=10, showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(title=title, hovermode='x unified')

    fig.show()

def plot_stock_price_trend_multi_same_scale(df, df2, title=None):
    
    df['收盘'] = df['收盘'] / df.loc[0, '收盘']
    df2['收盘'] = df2['收盘'] / df2.loc[0, '收盘']

    merged_df = pd.merge(df, df2, on='日期', how='inner', suffixes=('_股票', '_新曲线'))
    
    # 创建图表
    fig = go.Figure()
    
    # 添加股票收盘价曲线
    fig.add_trace(go.Scatter(x=merged_df['日期'], y=merged_df['收盘_股票'], mode='lines', name='df1'))
    
    # 添加新曲线
    fig.add_trace(go.Scatter(x=merged_df['日期'], y=merged_df['收盘_新曲线'], mode='lines', name='df2'))
    
    fig.update_xaxes(tickformat='%Y-%m-%d', nticks=10, showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(title='股票收盘价走势（相对起点调整）', hovermode='x unified')
    
    fig.show()


def plot_stock_price_trend_multi(df, df2, day=None,indicator=None):
    if day is None:
        day='日期'
    if indicator is None:
        indicator = '收盘'
    # 创建图表
    fig = go.Figure()

    # 添加股票收盘价曲线
    fig.add_trace(go.Scatter(x=df['日期'], y=df['收盘'], mode='lines+markers', name='股票收盘价'))

    # 添加新曲线，并使用第二个纵轴（y轴）
    fig.add_trace(
        go.Scatter(x=df2[day], y=df2[indicator], mode='lines+markers', name='新曲线', yaxis='y2'))

    # 设置第二个纵轴（y轴）
    fig.update_layout(yaxis2=dict(overlaying='y', side='right', showgrid=False, title='新曲线'))

    fig.update_xaxes(tickformat='%Y-%m-%d', nticks=10, showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(title='股票收盘价走势', hovermode='x unified')

    fig.show()