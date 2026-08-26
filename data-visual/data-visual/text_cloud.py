import cv2
import random
from pyecharts import options as opts
import pandas as pd
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Graph

# 从 CSV 文件中读取数据
file_path = r'../../database/shanhaijin.csv'
data = pd.read_csv(file_path)

# 排除symbolism列中值为未知的数据
filtered_data = data[data['symbolism'] != '未知']

# 将symbolism列的值拼接成一个字符串
symbolism_text = ' '.join(filtered_data['symbolism'])

# 统计词频
words = symbolism_text.split()
word_freq = {}
for word in words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# 将词频转换为适合的格式
wordcloud_data = [(word, freq) for word, freq in word_freq.items()]

# 读取凤凰图片并处理获取轮廓坐标
image_path = 'phoenix_shape.png'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 取最大的轮廓（假设凤凰是图片中最主要的元素）
main_contour = max(contours, key=cv2.contourArea)

# 将轮廓坐标转换为适合的格式
phoenix_shape_points = []
for point in main_contour.squeeze():
    phoenix_shape_points.append([int(point[0]), int(point[1])])

# 创建节点列表
nodes = []
for word, freq in wordcloud_data:
    # 随机生成颜色
    color = f"#{random.randint(0, 0xFFFFFF):06x}"
    nodes.append(
        {
            "name": word,
            "symbolSize": freq / 5,
            "symbol": "path://M" + " ".join([f"{x[0]} {x[1]}" for x in phoenix_shape_points]) + " Z",
            "label": {
                "show": True,
                "position": "inside",
                "formatter": word,
                "fontSize": 14,
                "color": color,
                "fontStyle": "italic",
                "textShadowBlur": 10,
                "textShadowColor": "rgba(0, 0, 0, 0.5)",
            },
            "itemStyle": {"color": color},
        }
    )

# 创建 Graph 图表
(
    Graph()
    .add(
        "",
        nodes,
        [],
        repulsion=5000,
        layout="force",  # 设置布局为力引导布局
        gravity=0.5,     # 设置节点受到的向中心的引力因子
        edge_length=5,  # 设置边长
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="球体词云图",
            subtitle="",
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=16,
                color="#333",
                font_weight="bold",
            ),
            subtitle_textstyle_opts=opts.TextStyleOpts(
                font_size=16,
                color="#666",
            ),
        ),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            trigger="item",
            formatter=JsCode(
                """
                function (params) {
                    return params.data.name + '<br/>词频: ' + params.data.symbolSize * 5;
                }
                """
            ),
        )
    )
    .render("../myproject/templates/html/insert/symbol/wordcloud_phoenix_custom.html")
)
