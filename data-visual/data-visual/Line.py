from pyecharts import options as opts
from pyecharts.charts import Line, Page

# 定义符合山海经特色的偏棕色系颜色
colors = ["#8B4513", "#A0522D", "#D2691E"]

# 创建文学折线图
line_literature = (
    Line(init_opts=opts.InitOpts(bg_color="transparent", width="600px", height="300px"))
    .add_xaxis(["文化", "美术书法雕塑与摄影", "语言", "历史"])
    .add_yaxis(
        "文学",
        [189, 147, 128, 124],
        linestyle_opts=opts.LineStyleOpts(color=colors[0]),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="文学相关分类数据"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="分类"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

# 创建科技折线图
line_technology = (
    Line(init_opts=opts.InitOpts(bg_color="transparent", width="600px", height="300px"))
    .add_xaxis(["艺术", "轻工业手工业", "医学", "计算机应用"])
    .add_yaxis(
        "科技",
        [41, 31, 29, 12],
        linestyle_opts=opts.LineStyleOpts(color=colors[1]),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="科技相关分类数据"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="分类"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

# 创建科学折线图
line_science = (
    Line(init_opts=opts.InitOpts(bg_color="transparent", width="600px", height="300px"))
    .add_xaxis(["生物", "自然科学理论与方法", "地质学", "天文学"])
    .add_yaxis(
        "科学",
        [12, 6, 6, 4],
        linestyle_opts=opts.LineStyleOpts(color=colors[2]),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="科学相关分类数据"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="分类"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

# 创建 Page 对象并添加图表
page = Page()
page.add(line_literature, line_technology, line_science)

# 渲染到 HTML 文件
page.render("./insert/value visualization/combined_charts.html")
