from pyecharts import options as opts
from pyecharts.charts import Map3D,Map
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode
import pymysql
import pandas as pd

# 数据库连接配置
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="shanhaijin",
    charset='utf8mb4'
)

try:
    cursor = conn.cursor()
    # 修正后的 SQL 查询语句
    query = """
    SELECT
  TRIM(
    SUBSTRING_INDEX(
      REPLACE(morden_location, '；', ';'),  -- 统一分号类型
      ';',
      1
    )
  ) AS province_group,
  COUNT(name) AS num
FROM shj
GROUP BY province_group;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    # 列名不需要反引号，直接与 SQL 中的别名对应
    df = pd.DataFrame(data, columns=["province_group", "num"])
    print(df.head())  # 测试输出
except pymysql.Error as e:
    print(f"数据库连接或查询出错: {e}")
    df = pd.DataFrame()  # 防止 NameError，初始化空 DataFrame
finally:
    if conn:
        conn.close()

# 定义中国省份列表（包括省、自治区、直辖市）
china_provinces = [
    '北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省',
    '黑龙江省',
    '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
    '河南省',
    '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市',
    '四川省', '贵州省',
    '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区',
    '新疆维吾尔自治区', '台湾省'
]

# 定义省份经纬度字典
province_coordinates = {
    '北京市': [116.4074, 39.9042],
    '天津市': [117.1902, 39.1255],
    '河北省': [114.4995, 38.1006],
    '山西省': [112.5492, 37.8570],
    '内蒙古自治区': [111.7656, 40.8175],
    '辽宁省': [123.4291, 41.7968],
    '吉林省': [125.3245, 43.8868],
    '黑龙江省': [126.6425, 45.7560],
    '上海市': [121.4737, 31.2304],
    '江苏省': [118.7674, 32.0415],
    '浙江省': [120.1536, 30.2875],
    '安徽省': [117.2830, 31.8612],
    '福建省': [119.2965, 26.0998],
    '江西省': [115.8922, 28.6765],
    '山东省': [117.0009, 36.6758],
    '河南省': [113.6654, 34.7570],
    '湖北省': [114.2986, 30.5844],
    '湖南省': [112.9823, 28.1941],
    '广东省': [113.2665, 23.1322],
    '广西壮族自治区': [108.3200, 22.8240],
    '海南省': [110.1999, 20.0442],
    '重庆市': [106.5049, 29.5332],
    '四川省': [104.0758, 30.6516],
    '贵州省': [106.7135, 26.5783],
    '云南省': [102.7123, 25.0406],
    '西藏自治区': [91.1174, 29.6442],
    '陕西省': [108.9480, 34.2632],
    '甘肃省': [103.8342, 36.0610],
    '青海省': [101.7800, 36.6209],
    '宁夏回族自治区': [106.2590, 38.4722],
    '新疆维吾尔自治区': [87.6168, 43.8256],
    '台湾省': [121.5091, 25.0443]
}

# 为特殊分类添加经纬度
special_coordinates = {
    '非中国地区': [130, 30],  # 中国地图旁边
    '地理区域': [110, 50],  # 中国地图上边
    '未知地区': [70, 55]  # 整个地图左上角
}

# 定义分类函数
def classify_region(region):
    # 检查是否为中国省份
    for province in china_provinces:
        if province in region:
            return province

    # 检查是否为非中国地区
    non_china_regions = ['东海', '中亚地区', '印度', '日本', '朝鲜半岛', '越南']
    if region in non_china_regions:
        return '非中国地区'

    # 检查是否为山脉/高原/地理区域
    geo_regions = ['昆仑山脉', '巫山', '蒙古高原', '辽东地区', '研州山',
                   '楚之北境']
    if region in geo_regions:
        return '地理区域'

    # 检查是否为未知地区
    if region == '未知':
        return '未知地区'

    # 如果地区包含"省"或"县"等字样但未匹配到具体省份，归类为"其他中国地区"
    if '省' in region or '县' in region or '市' in region:
        return '地理区域'

    # 默认归类为"其他"
    return '未知'
# 应用分类函数
df['分类'] = df['province_group'].apply(classify_region)

# 统计各分类的数量
result = df.groupby('分类')['num'].sum().reset_index()

# 转换为指定格式
final_result = []
for index, row in result.iterrows():
    category = row['分类']
    count = row['num']
    if category in province_coordinates:
        coordinates = province_coordinates[category]
        final_result.append((category, coordinates + [count]))
    elif category in special_coordinates:
        coordinates = special_coordinates[category]
        final_result.append((category, coordinates + [count]))
    else:
        final_result.append((category, ["未知", "未知", count]))

# 创建 3D 地图
c = (
    Map3D(init_opts=opts.InitOpts(bg_color="transparent", chart_id="china_map_3d"))
    .add_schema(
        itemstyle_opts=opts.ItemStyleOpts(
            color="#556B2F",
            opacity=1,
            border_width=0.8,
            border_color="#DAA520",
        ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=False,
            formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
        ),
        emphasis_label_opts=opts.LabelOpts(
            is_show=False,
            color="#E5E5E5",
            font_size=10,
            background_color="rgba(0,23,11,0)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#FFD700",
            main_intensity=1.2,
            main_shadow_quality="high",
            is_main_shadow=False,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    )
    .add(
        series_name="bar3D",
        data_pair=final_result,
        type_=ChartType.BAR3D,
        bar_size=1,
        shading="lambert",
        label_opts=opts.LabelOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        itemstyle_opts=opts.ItemStyleOpts(
            color="rgba(218,165,32,0.8)"
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="山海经奇物地理位置统计图", pos_left="left",
                                  title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),),
        visualmap_opts=opts.VisualMapOpts(is_show=False),
    )
    # .add_js_funcs("""
    #     // 点击事件
    #     echarts.getInstanceByDom(document.getElementById('china_map_3d')).on('click', function(params) {
    #         var provinceMap = {
    #             '北京市': 'beijing.html',
    #             '天津市': 'tianjin.html',
    #             '河北省': 'hebei.html',
    #             '山西省': 'shanxi1.html',
    #             '内蒙古自治区': 'neimenggu.html',
    #             '辽宁省': 'liaoning.html',
    #             '吉林省': 'jilin.html',
    #             '黑龙江省': 'heilongjiang.html',
    #             '上海市': 'shanghai.html',
    #             '江苏省': 'jiangsu.html',
    #             '浙江省': 'zhejiang.html',
    #             '安徽省': 'anhui.html',
    #             '福建省': 'fujian.html',
    #             '江西省': 'jiangxi.html',
    #             '山东省': 'shandong.html',
    #             '河南省': 'henan.html',
    #             '湖北省': 'hubei.html',
    #             '湖南省': 'hunan.html',
    #             '广东省': 'guangdong.html',
    #             '海南省': 'hainan.html',
    #             '重庆市': 'chongqing.html',
    #             '四川省': 'sichuan.html',
    #             '贵州省': 'guizhou.html',
    #             '云南省': 'yunnan.html',
    #             '西藏自治区': 'xizang.html',
    #             '陕西省': 'shanxi2.html',
    #             '甘肃省': 'gansu.html',
    #             '青海省': 'qinghai.html',
    #             '宁夏回族自治区': 'ningxia.html',
    #             '新疆维吾尔自治区': 'xinjiang.html',
    #             '香港特别行政区': 'hongkong.html',
    #             '澳门特别行政区': 'aomen.html',
    #             '台湾省': 'taiwan.html',
    #             '非中国地区': 'non_china.html',
    #             '地理区域': 'geo_region.html',
    #             '未知地区': 'unknown_region.html'
    #         };
    #
    #         // 跳转逻辑
    #         if (provinceMap[params.name]) {
    #             window.location.href = provinceMap[params.name];
    #         } else {
    #             console.log('未找到对应的跳转页面: ' + params.name);
    #         }
    #     });
    # """)
)

# 生成 HTML 文件
c.render("../myproject/templates/html/Map/china_map_3D.html")

# 定义数据点的大小函数
# 假设 heatmap_data 是你的数据列表
heatmap_data = [(item[0], item[1][2]) for item in final_result]

# 创建 Map 对象
(
    Map(init_opts=opts.InitOpts(bg_color="transparent"))
    .add(
        series_name="省份数据",
        data_pair=heatmap_data,
        maptype="china",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国省份热力地图"),
        visualmap_opts=opts.VisualMapOpts(min_=min([data[1] for data in heatmap_data]),
                                          max_=max([data[1] for data in heatmap_data])),
        tooltip_opts=opts.TooltipOpts(trigger="item"),
    )
).render("./insert/map/2D热力统计图.html")
heatmap_data = [(item[0], item[1][2]) for item in final_result]
# 提取省份名和数量
provinces = [data[0] for data in heatmap_data]
quantities = [data[1] for data in heatmap_data]
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
c = (
    PictorialBar()
    .add_xaxis(provinces)
    .add_yaxis(
        "",
        quantities,
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=18,
        symbol_repeat="fixed",
        symbol_offset=[0, 0],
        is_symbol_clip=True,
        symbol=SymbolType.ROUND_RECT,
    )
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各位置异兽数量象形柱图"),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
        datazoom_opts=[  # 添加垂直拖动轴配置
            opts.DataZoomOpts(
                orient="vertical",       # 垂直方向
                type_="slider",          # 滑动条模式
                range_start=0,           # 起始显示比例
                range_end=50,            # 初始显示50%数据
            )
        ],
    )
)
c.render("./insert/map/province_quantity_horizontal_pictorialbar.html")