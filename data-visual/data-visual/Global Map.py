import pyecharts.options as opts
from pyecharts.charts import MapGlobe, Timeline

# 基础数据和现代数据
base_data = {
    "China": 18, "Greece": 5, "Saudi Arabia": 3,
    "Italy": 2, "India": 1, "Germany": 2,
    "France": 1, "Japan": 1, "Russia": 2
}

modern_data = {
    "China": 38000, "UK": 12000,
    "United States": 15000, "Germany": 8000,
    "France": 6000, "Japan": 5000, "Russia": 4500,
    "Australia": 3000, "India": 2500, "Italy": 2000,
    "Republic of Korea": 1800,
    "Canada": 2200, "Brazil": 1500
}

# 创建一个包含国家经纬度信息的字典
coordinates = {
    "China": [35.8617, 104.1954],
    "Greece": [39.0742, 21.8243],
    "Saudi Arabia": [23.8859, 45.0792],
    "Italy": [41.8719, 12.5674],
    "India": [20.5937, 78.9629],
    "Germany": [51.1657, 10.4515],
    "France": [46.6034, 1.8883],
    "Japan": [36.2048, 138.2529],
    "Russia": [61.5240, 105.3188],
    "UK": [55.3781, -3.4360],
    "United States": [37.0902, -95.7129],
    "Australia": [-25.2744, 133.7751],
    "Republic of Korea": [35.9078, 127.7669],
    "Canada": [56.1304, -106.3468],
    "Brazil": [-14.2350, -51.9253]
}

# 合并所有数据以获取最小值和最大值
all_data = list(base_data.values()) + list(modern_data.values())
low, high = min(all_data), max(all_data)

# 创建时间轴对象
timeline = Timeline()


# 定义一个函数来创建地图
def create_map(data, title):
    map_globe = (
        MapGlobe()
        .add_schema()
        .add(
            maptype="world",
            series_name="著作数量",
            data_pair=list(data.items()),
            is_map_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(border_width=0.8, border_color="rgba(0,0,0,0.2)"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(
                min_=low,
                max_=high,
                range_text=["max", "min"],
                is_calculable=True,
                range_color=["lightskyblue", "yellow", "orangered"],
            )
        )
    )
    return map_globe


# 添加基础数据的地图
timeline.add(create_map(base_data, "基础时期著作数量分布"), "基础时期")

# 添加现代数据的地图
timeline.add(create_map(modern_data, "现代时期著作数量分布"), "现代时期")

# 渲染时间轴地图
timeline.render("./insert/3D/time_varying_map_globe.html")
