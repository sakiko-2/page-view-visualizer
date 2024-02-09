import calendar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

pageviews_filepath = 'fcc-forum-pageviews.csv'
df = pd.read_csv(pageviews_filepath, index_col='date', parse_dates=True)

df = df[(df.value >= df.value.quantile(0.025)) & (df.value <= df.value.quantile(0.975))]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df.index, df.value, color='tab:red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar = df_bar.groupby([df.index.year, df.index.month]).mean().unstack()

    fig, ax = plt.subplots(figsize=(8, 7))
    width = 0.05
    multiplier = 0

    for month, y in df_bar.items():
        offset = width * multiplier
        x = np.arange(len(df_bar.index))
        ax.bar(x + offset, y, width, label=calendar.month_name[month[1]])
        multiplier += 1

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_xticks(x + width * len(df_bar.keys()) / 2 - 0.025, df_bar.index, rotation='vertical')
    ax.legend(loc='upper left', title='Months')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months = [calendar.month_abbr[d] for d in list(range(1, 13))]

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6), layout='constrained')
    sns.boxplot(data=df_box, x=df_box.year, y=df_box.value, ax=ax1, palette='tab10', flierprops={'marker': 'd'}, fliersize=1)
    ax1.set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)', yticks=np.arange(0, 200000.1, 20000))
    sns.boxplot(data=df_box, x=df_box.month, y=df_box.value, ax=ax2, palette='husl', flierprops={'marker': 'd'}, fliersize=1, order=months)
    ax2.set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)', yticks=np.arange(0, 200000.1, 20000))

    fig.get_layout_engine().set(w_pad=0.35, h_pad=0.35)

    fig.savefig('box_plot.png')
    return fig
