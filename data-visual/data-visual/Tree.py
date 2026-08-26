from pyecharts import options as opts
from pyecharts.charts import Tree
from pyecharts.globals import ThemeType
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv(r'../../database/shanhaijin.csv')

# 去除章节中的未知值
filtered_df = df[df['chapter']!= '未知'].copy()

# 规范章节名称
def standardize_chapter(chapter):
    if '山经' in chapter:
        return '山经'
    elif '海内经' in chapter:
        return '海内经'
    elif '海外经' in chapter:
        return '海外经'
    elif '大荒经' in chapter:
        return '大荒经'
    return None

# 使用.loc 来设置值，避免警告
filtered_df.loc[:, 'chapter'] = filtered_df['chapter'].apply(standardize_chapter)
# 去除非目标章节的数据
filtered_df = filtered_df[filtered_df['chapter'].notnull()]

# 创建树状图数据结构
tree_data = [
    {
        "children": [],
        "name": "山海经",
        "itemStyle": {"color": "#8B4513"}  # 为根节点设置颜色，这里使用类似棕褐色代表山海经主题
    }
]

# 按章节分组
for chapter in filtered_df['chapter'].unique():
    chapter_data = {
        "name": chapter,
        "children": [],
        "itemStyle": {"color": "#CD853F"}  # 为章节节点设置颜色，类似浅棕色
    }
    chapter_df = filtered_df[filtered_df['chapter'] == chapter]

    # 按科属分组
    for category in chapter_df['category'].unique():
        category_data = {
            "name": category,
            "children": []
        }
        category_df = chapter_df[chapter_df['category'] == category]

        # 添加异兽名称
        for _, row in category_df.iterrows():
            name_data = {
                "name": row['name']
            }
            category_data['children'].append(name_data)

        chapter_data['children'].append(category_data)

    tree_data[0]["children"].append(chapter_data)

# 创建树状图，使用 LIGHT 主题
c = (
    Tree(init_opts=opts.InitOpts(theme=ThemeType.LIGHT,bg_color="transparent"))
    .add(
        series_name="",
        data=tree_data,
        label_opts=opts.LabelOpts(position="top", color="#000000"),  # 设置标签颜色为黑色
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="山海经章节、异兽科属与名称树形图"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )
)

# 渲染图表
c.render("./insert/data visual analysis/tree_shanhaijin_category_name.html")