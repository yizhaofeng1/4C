from pyecharts import options as opts
from pyecharts.charts import Pie
import pandas as pd
# 加载数据
df = pd.read_csv(r'../../database/shanhaijin.csv')
# 定义一个函数来对 chapter 进行分类
def categorize_chapter(chapter):
    if '山经' in chapter:
        return '山经'
    elif '海内经' in chapter:
        return '海内经'
    elif '海外经' in chapter:
        return '海外经'
    elif '大荒经' in chapter:
        return '大荒经'
    else:
        return '未知'
# 对 chapter 列进行分类
df['chapter_category'] = df['chapter'].apply(categorize_chapter)
# 统计每个类别的异兽数量
count_by_category = df['chapter_category'].value_counts().reset_index(name='异兽数量')
# 使用 pyecharts 绘制玫瑰图
pie = (
    Pie(init_opts=opts.InitOpts(bg_color="transparent"))
    .add(
        "",
        [list(z) for z in zip(count_by_category['chapter_category'], count_by_category['异兽数量'])],
        radius=["30%", "75%"],
        center=["50%", "50%"],
        rosetype="radius",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="不同类别异兽数量玫瑰图"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
    )
)

# 渲染为 HTML 文件
pie.render("./insert/data visual analysis/strange_creatures_rose_chart.html")