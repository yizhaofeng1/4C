import pandas as pd
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Bar3D
from pyecharts.commons.utils import JsCode
# 数据库连接配置
conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="shanhaijin",
        charset='utf8mb4'
)
cursor = conn.cursor()
# SQL 查询语句
query = """
        SELECT TRIM(mountain_location) AS mountain_location, COUNT(*) AS value
        FROM shj
        WHERE TRIM(mountain_location) != ''
        GROUP BY mountain_location
        ORDER BY value DESC;
        """
cursor.execute(query)
data = cursor.fetchall()
df = pd.DataFrame(data, columns=["mountain_location", "value"])
cursor.close()

# 若查询成功，继续处理数据
if 'df' in locals():
    # 定义方向到 (x, y) 坐标的映射
    direction_to_xy = {
        '北': (0, 1),
        '东北': (1, 1),
        '东': (1, 0),
        '东南': (1, -1),
        '南': (0, -1),
        '西南': (-1, -1),
        '西': (-1, 0),
        '西北': (-1, 1),
        '中': (0, 0),
        '未知': (0, 0),
        '不详': (0, 0),
        '南海': (0, -1)
    }

    directions = {d: 0 for d in direction_to_xy.keys()}
    for _, row in df.iterrows():
        loc = row['mountain_location']
        if loc in directions:
            directions[loc] += row['value']
        else:
            directions['未知'] += row['value']

    # 准备 3D 图表数据
    data_3d = []
    for direction, value in directions.items():
        x, y = direction_to_xy[direction]
        data_3d.append([x, y, value])
    # 【优化1】使用更具神话感的颜色光谱（深紫 → 天青 → 翠绿 → 鎏金 → 赤红）
    mythical_colors = [
        "#4B0082", "#6A5ACD", "#4682B4", "#00CED1",
        "#20B2AA", "#32CD32", "#9ACD32", "#FFD700",
        "#DAA520", "#FF8C00", "#CD5C5C"
    ]

    # 【优化2】调整背景为玄天色 + 增加网格线
    bg_color = "#0A122A"  # 深空蓝
    grid_color = "rgba(200, 200, 200, 0.2)"  # 半透明白

    # 【优化3】重新设计坐标轴样式
    axis_style = {
        "axislabel_opts": opts.LabelOpts(color="#E6DAA6"),  # 关键修正：axislabel → axislabel_opts
        "axisline_opts": opts.AxisLineOpts(  # 关键修正：axisline → axisline_opts
            linestyle_opts=opts.LineStyleOpts(color="#808080", width=2)
        ),
        "axistick_opts": opts.AxisTickOpts(is_show=False)  # 关键修正：axistick → axistick_opts
    }
    zaxis_config = opts.Axis3DOpts(
        type_="value",
        name="频次",
        **axis_style,  # 直接应用统一样式
    )

    # 创建 3D 柱形图
    (
        Bar3D(init_opts=opts.InitOpts(bg_color="transparent", width="100%", height="350px"))
        .add(
            series_name="方位计数",
            data=data_3d,
            xaxis3d_opts=opts.Axis3DOpts(type_="value", name="东 ← 经度 → 西", **axis_style),
            yaxis3d_opts=opts.Axis3DOpts(type_="value", name="北 ← 纬度 → 南", **axis_style),
            zaxis3d_opts=zaxis_config  # 使用修正后的 Z 轴配置
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=max([item[2] for item in data_3d]),
                range_color=mythical_colors,
            ),
            title_opts=opts.TitleOpts(title="方向统计 3D 柱形图"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=JsCode("""
                        function(params) {
                            var directionMap = {
                                '0,1': '北',
                                '1,1': '东北',
                                '1,0': '东',
                                '1,-1': '东南',
                                '0,-1': '南',
                                '-1,-1': '西南',
                                '-1,0': '西',
                                '-1,1': '西北',
                                '0,0': '中/未知'
                            };
                            var x = params.value[0];
                            var y = params.value[1];
                            var key = x + ',' + y;
                            return '方位: ' + (directionMap[key] || '未知') + '<br/>数量: ' + params.value[2];
                        }
                    """)
            )
        )
        .render("../myproject/templates/html/insert/map/direction_statistics_3d_bar.html")
    )


