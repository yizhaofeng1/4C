from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Line, Page
import pandas as pd

# 从 CSV 文件中读取数据
file_path =r'../../database/shanhaijin.csv'
df = pd.read_csv(file_path)

# 把非东南西北及其组合的方位归为其他
def categorize_direction(direction):
    valid_directions = ['东', '南', '西', '北', '东南', '东北', '西南', '西北']
    if direction in valid_directions:
        return direction
    return '其他'

df['direction_category'] = df['mountain_location'].apply(categorize_direction)

# 统计不同方位的异兽数量和类别数量
grouped_data = df.groupby('direction_category').agg(
    num_creatures=('name', 'nunique'),
    num_categories=('category', 'nunique')
).reset_index()

# 定义符合山海经风格的偏棕色系颜色
colors = ['#8B4513', '#D2691E', '#A0522D', '#CD853F', '#F4A460', '#DEB887', '#BC8F8F', '#DAA520']

# 创建方位饼形图
pie = (
    Pie(init_opts=opts.InitOpts(bg_color="transparent"))
    .add(
        "",
        [list(z) for z in zip(grouped_data['direction_category'], grouped_data['num_creatures'])],
        radius=["30%", "75%"],
    )
    .set_colors(colors)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="不同方位异兽数量占比饼图"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# 创建方位 - 异兽数量折线图和方位 - 类别数量柱形图
bar = (
    Bar(init_opts=opts.InitOpts(bg_color="transparent"))
    .add_xaxis(grouped_data['direction_category'].tolist())
    .add_yaxis("类别数量", grouped_data['num_categories'].tolist(), color=colors[0])
)

# 动态计算异兽数量 Y 轴的刻度间隔
max_num = grouped_data['num_creatures'].max()
interval = 20  # 可根据实际情况调整，这里设为 20 使刻度更清晰

bar.extend_axis(
    yaxis=opts.AxisOpts(
        name="异兽数量",
        type_="value",
        min_=0,
        max_=max_num + 10,  # 留一定余量
        interval=interval,
        axislabel_opts=opts.LabelOpts(formatter="{value}")
    )
)

line = (
    Line()
    .add_xaxis(grouped_data['direction_category'].tolist())
    .add_yaxis("异兽数量", grouped_data['num_creatures'].tolist(), yaxis_index=1, color=colors[1])
)

bar.overlap(line)

# 使用 Page 组合图表
page = Page()
page.add(pie, bar)
page.render("./insert/data visual analysis/combined_charts_new.html")