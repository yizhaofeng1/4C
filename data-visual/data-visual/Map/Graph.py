from pyecharts import options as opts
from pyecharts.charts import Graph, Map
import os
import pandas as pd
import shutil

# 获取当前工作目录
path = os.getcwd()

# 导入文件
file_path = r'../../../shanhaijin/jisuanji sheji dasai/database/shanhaijin.csv'
file = pd.read_csv(file_path)

# 定义一个函数来创建文件夹
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 为每个省份生成单独的地图
provinces = [
    "北京", "天津", "上海", "重庆",
    "河北", "山西", "辽宁", "吉林",
    "黑龙江", "江苏", "浙江", "安徽",
    "福建", "江西", "山东", "河南",
    "湖北", "湖南", "广东", "海南",
    "四川", "贵州", "云南", "陕西",
    "甘肃", "青海", "内蒙古", "广西",
    "西藏", "宁夏", "新疆", "台湾",
    "香港", "澳门"
]

for province in provinces:
    (
        Map()
       .add(
            series_name="",
            data_pair=[(province, 1)],  # 给对应省份一个值用于区分显示
            maptype=province,  # 关键，指定地图类型为对应省份
            label_opts=opts.LabelOpts(is_show=False)  # 不显示标签
        )
       .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{province}地图"),
            visualmap_opts=opts.VisualMapOpts(
                max_=1,  # 因前面数据值设为1，最大值设为1
                range_color=["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
            )
        )
       .render(f"{province}_map.html")
    )

# 循环生成关系图
for i in range(len(file)):
    graph = Graph(init_opts=opts.InitOpts(bg_color="transparent"))
    # 获取数据
    name = file.iloc[i, 0]
    appearance = file.iloc[i, 1]
    original_habitat = file.iloc[i, 2]
    modern_location = file.iloc[i, 3].split(";")[0][:2]
    abilities = file.iloc[i, 6]
    symbolism = file.iloc[i, 7]
    category = file.iloc[i, 8]

    # 检查文件夹是否存在
    folder_path = os.path.join(path, modern_location)
    create_folder(folder_path)

    info = [
        {"id": name, "name": name},
        {"id": appearance, "name": appearance},
        {"id": original_habitat, "name": original_habitat},
        {"id": modern_location, "name": modern_location},
        {"id": abilities, "name": abilities},
        {"id": symbolism, "name": symbolism},
        {"id": category, "name": category}
    ]
    coo = [
        {"source": name, "target": appearance},
        {"source": name, "target": original_habitat},
        {"source": name, "target": modern_location},
        {"source": name, "target": abilities},
        {"source": name, "target": symbolism},
        {"source": name, "target": category}
    ]

    graph.add(
        series_name=f"{name}",
        nodes=info,
        links=coo,
        repulsion=200,  # 增大节点间斥力使间隔变大
        linestyle_opts=opts.LineStyleOpts(curve=0.5, color='gold'),
        itemstyle_opts=opts.ItemStyleOpts(color='gold')
    )

    graph.render(os.path.join(folder_path, f"{name}.html"))

    # 将对应省份的地图复制到该省份文件夹中
    map_file = f"{modern_location}_map.html"
    if os.path.exists(map_file):
        shutil.copy(map_file, folder_path)