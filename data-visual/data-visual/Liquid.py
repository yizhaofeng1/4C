from pyecharts import options as opts
from pyecharts.charts import Liquid
from pyecharts.globals import SymbolType
import pandas as pd
# 计算 modern_location 列中值不为未知的数量
# 加载数据
df = pd.read_csv(r'../../database/shanhaijin.csv')
not_unknown_count = df[df['modern_location'] != '未知']['modern_location'].count()

# 计算占比
percentage = not_unknown_count / df['modern_location'].count()

# 创建水滴图
(
    Liquid(init_opts=opts.InitOpts(bg_color="transparent"))
    .add(
        "lq",
        [percentage],
        is_outline_show=False,
        shape=SymbolType.DIAMOND,
        background_color="rgba(0,0,0,0)",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="地理位置落实占比"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(is_show=False),
    )
    .render("./insert/data-visual-analysis/liquid_shape_diamond.html")
)

print(f'modern_location列不是未知的值所占百分比: {percentage * 100}%')