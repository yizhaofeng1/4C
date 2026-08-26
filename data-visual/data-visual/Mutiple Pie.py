import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

# 加载数据，需要将文件路径替换为你的实际路径
df = pd.read_csv(r'../../database/shanhaijin.csv')

# 统计各个 category 的数量
category_counts = df['category'].value_counts().reset_index(name='数量')

# 使用 pyecharts 创建饼图
pie = (
    Pie(init_opts=opts.InitOpts(bg_color="transparent"))
    .add(
        "",
        [list(z) for z in zip(category_counts['category'], category_counts['数量'])],
        radius=["30%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各个 category 的数量占比"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
    )
)

# 渲染图表
pie.render("./insert/data visual analysis/category_counts_pie_chart.html")