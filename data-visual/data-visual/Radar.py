import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Radar

# 从 CSV 文件中读取数据
df = pd.read_csv(r'../../database/shanhaijin.csv')

# 处理章节相关统计及绘图
# 定义函数来执行统计操作
def count_chapters(category_filter, category_name):
    filtered_df = df[df['category'].isin(category_filter)]
    shanjing = filtered_df['chapter'].str.contains('山经').sum()
    hainei = filtered_df['chapter'].str.contains('海内').sum()
    haiwai = filtered_df['chapter'].str.contains('海外').sum()
    dahuang = filtered_df['chapter'].str.contains('大荒').sum()
    unknown = filtered_df[~filtered_df['chapter'].str.contains('山经') &
                          ~filtered_df['chapter'].str.contains('海内') &
                          ~filtered_df['chapter'].str.contains('海外') &
                          ~filtered_df['chapter'].str.contains('大荒')].shape[0]
    return pd.DataFrame({
        'category': [category_name],
        '山经': [shanjing],
        '海内经': [hainei],
        '海外经': [haiwai],
        '大荒经': [dahuang],
        '未知': [unknown]
    })


# 执行各个分类的统计并合并结果
result = pd.concat([
    count_chapters(['植物'], '植物'),
    count_chapters(['超自然生物', '混合形态或超自然生物'],
                   '混合形态或超自然生物'),
    count_chapters(['鸟类'], '鸟类'),
    count_chapters(['爬行与蛇类'], '爬行与蛇类'),
    count_chapters(['人类', '兽类', '人类异种', '神怪'], '兽类'),
    count_chapters(['无', '山', '矿物', '未知'], '未知'),
    count_chapters(['鱼类与水生生物'], '鱼类与水生生物')
], ignore_index=True)

# 对数值列保留一位小数
numeric_columns = result.columns[1:]
result[numeric_columns] = result[numeric_columns].astype(float).round(1)

# 修正后的基础配置
schema_chapter = [
    {"name": "山经", "max": result['山经'].max()+5},
    {"name": "海内经", "max": result['海内经'].max()+5},
    {"name": "海外经", "max": result['海外经'].max()+5},
    {"name": "大荒经", "max": result['大荒经'].max()+5},
    {"name": "未知", "max": result['未知'].max()+5}
]

# 从统计结果中获取数据集
data_config_chapter = []
colors = ["#2ca02c", "#ff7f0e", "#1f77b4", "#d62728", "#9467bd", "#8c564b",
          "#4e79a7"]
for i, row in result.iterrows():
    category = row['category']
    values = [list(row[1:])]
    color = colors[i % len(colors)]
    data_config_chapter.append((category, values, color))

# 创建雷达图（修正关键参数）
radar_chapter = (
    Radar(init_opts=opts.InitOpts(
        page_title="山海经生物分布雷达图",
        bg_color="transparent",
        width="280px",
        height="250px"
    ))
    .add_schema(
        schema=schema_chapter,
        radius="75%",
        center=["65%", "48%"],  # 调整中心点位置
        splitarea_opt=opts.SplitAreaOpts(is_show=True,
                                         areastyle_opts=opts.AreaStyleOpts(
                                             opacity=0.1)),
        textstyle_opts=opts.TextStyleOpts(color="#333", font_size=12),
        splitline_opt=opts.SplitLineOpts(is_show=True,
                                         linestyle_opts=opts.LineStyleOpts(
                                             width=1)),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="山海经生物分布",
                                  subtitle="按分类和地理经卷统计"),
        legend_opts=opts.LegendOpts(
            pos_right="8%",
            pos_top="1%",
            selected_mode="multiple",
            item_width=25,  # 调整图例样式
            item_height=25
        ))
)

# 修正后的数据系列添加方式
for name, value, color in data_config_chapter:
    radar_chapter.add(
        series_name=name,
        data=value,
        color=color,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.4 if name != "未知" else 0),
        linestyle_opts=opts.LineStyleOpts(
            width=3,
            type_="solid",  # 明确指定线型
            # 通过修改线条属性增强数据点显示
            color=color,
            opacity=0.8
        )
    )

radar_chapter.render("../myproject/templates/html/insert/map/scriptures.html")

# 处理方向相关统计及绘图
# 定义方向统计函数
def calculate_directions(df_part):
    directions = ['东', '西', '南', '北', '中', '未知']
    result = {}

    # 显式创建副本避免链式索引警告
    df_part = df_part.copy()  # 关键修正点

    for dir in directions[:4]:  # 处理东南西北
        df_part[dir] = df_part['mountain_location'].apply(
            lambda x:
            1 if x == dir else
            0.5 if dir in str(x) and len(str(x)) > 1 else
            0
        )
        result[dir] = df_part[dir].sum()

    # 处理中
    result['中'] = df_part['mountain_location'].apply(
        lambda x: 1 if x == '中' else 0
    ).sum()

    # 处理未知
    result['未知'] = df_part[
        (~df_part['mountain_location'].isin(['东', '西', '南', '北', '中'])) &
        (~df_part['mountain_location'].str.contains('东|西|南|北', na=False))
    ].shape[0]

    return pd.Series(result)


# 定义分类逻辑
categories = [
    ('植物', ['植物']),
    ('混合形态或超自然生物', ['超自然生物', '混合形态或超自然生物']),
    ('鸟类', ['鸟类']),
    ('爬行与蛇类', ['爬行与蛇类']),
    ('兽类', ['人类', '兽类', '人类异种', '神怪']),
    ('未知', ['无', '山', '矿物', '未知']),
    ('鱼类与水生生物', ['鱼类与水生生物'])
]

# 计算结果
results = []
for cat_name, cat_list in categories:
    if cat_name == '混合形态或超自然生物':  # 处理特殊分类
        # 显式创建副本避免链式索引警告
        df_part = df[df['category'].isin(cat_list) | (
                df['category'] == '混合形态或超自然生物')].copy()  # 关键修正点
    else:
        # 显式创建副本避免链式索引警告
        df_part = df[df['category'].isin(cat_list)].copy()  # 关键修正点

    stats = calculate_directions(df_part)
    stats['category'] = cat_name
    results.append(stats)

# 合并结果
final_df = pd.DataFrame(results)[
    ['category', '东', '西', '南', '北', '中', '未知']]

# 根据处理后的数据生成雷达图所需的数据配置
schema_direction = [
    {"name": "东", "max": final_df['东'].max()+5},
    {"name": "西", "max": final_df['西'].max()+5},
    {"name": "南", "max": final_df['南'].max()+5},
    {"name": "北", "max": final_df['北'].max()+5},
    {"name": "中", "max": final_df['中'].max()+5},
    {"name": "未知", "max": final_df['未知'].max()+5}
]

data_config_direction = []
color_map = {  # 统一管理颜色映射
    "植物": "#2ca02c",
    "兽类": "#ff7f0e",
    "鱼类与水生生物": "#1f77b4",
    "鸟类": "#d62728",
    "混合形态或超自然生物": "#9467bd",
    "爬行与蛇类": "#8c564b",
    "未知": "#4e79a7"
}
for _, row in final_df.iterrows():
    cat_name = row['category']
    values = [row['东'], row['西'], row['南'], row['北'], row['中'],
              row['未知']]
    data_config_direction.append((cat_name, [values], color_map[cat_name]))

# 创建雷达图
radar_direction = (
    Radar(init_opts=opts.InitOpts(
        page_title="山海经生物分布雷达图",
        bg_color="transparent",
        width="280px",
        height="250px"
    ))
    .add_schema(
        schema=schema_direction,
        radius="75%",
        center=["65%", "48%"],
        splitarea_opt=opts.SplitAreaOpts(is_show=True,
                                         areastyle_opts=opts.AreaStyleOpts(
                                             opacity=0.1)),
        textstyle_opts=opts.TextStyleOpts(color="#333", font_size=12),
        splitline_opt=opts.SplitLineOpts(is_show=True,
                                         linestyle_opts=opts.LineStyleOpts(
                                             width=1)),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="山海经生物分布",
                                  subtitle="按分类和地理方向统计"),
        legend_opts=opts.LegendOpts(
            pos_right="8%",
            pos_top="1%",
            selected_mode="multiple",
            item_width=25,
            item_height=25
        )
    )
)

# 添加数据系列
for name, value, color in data_config_direction:
    radar_direction.add(
        series_name=name,
        data=value,
        color=color,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.4 if name != "未知" else 0),
        linestyle_opts=opts.LineStyleOpts(
            width=3,
            type_="solid",
            color=color,
            opacity=0.8
        )
    )

radar_direction.render("../myproject/templates/html/insert/map/Genus.html")