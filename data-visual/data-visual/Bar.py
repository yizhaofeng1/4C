import pandas as pd
import pymysql
from pyecharts.charts import Bar, Timeline
from pyecharts import options as opts
try:
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
    SELECT 
        -- 根据 chapter 列进行分类
        CASE 
            WHEN TRIM(chapter) LIKE '%山经%' THEN '山经'
            WHEN TRIM(chapter) LIKE '%海内经%' THEN '海内经'
            WHEN TRIM(chapter) LIKE '%海外经%' THEN '海外经'
            WHEN TRIM(chapter) LIKE '%大荒经%' THEN '大荒经'
            ELSE '未知'
        END AS category_classified,
        -- 提取 modern_location 列的前两个字符作为省份
        SUBSTR(TRIM(morden_location), 1, 2) AS province,
        COUNT(*) AS count
    FROM 
        shj
    GROUP BY 
        category_classified, province
    ORDER BY 
        category_classified, province;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    result = pd.DataFrame(data, columns=["category_classified", "province", "count"])

except pymysql.Error as e:
    print(f"数据库连接或查询出错：{e}")
finally:
    if conn:
        conn.close()
# 创建 TimeLine 对象
timeline = Timeline()

# 遍历每个分类
for category in result['category_classified'].unique():
    category_data = result[result['category_classified'] == category]
    # 按省份排序
    category_data = category_data.sort_values(by='province')
    provinces = category_data['province'].tolist()
    counts = category_data['count'].tolist()

    # 创建柱状图
    bar = Bar(init_opts=opts.InitOpts(bg_color="transparent"))
    bar.add_xaxis(provinces)
    bar.add_yaxis("书中分布数量", counts)

    # 设置全局选项
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{category} 各省份异兽数量分布"),
        xaxis_opts=opts.AxisOpts(name="省份"),
        yaxis_opts=opts.AxisOpts(name="数量"),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )

    # 将柱状图添加到 TimeLine 中
    timeline.add(bar, time_point=category)

# 设置 TimeLine 的播放选项
timeline.add_schema(
    play_interval=1000,
    is_auto_play=True,
    is_loop_play=True,
    is_timeline_show=True
)

# 渲染图表
timeline.render("./insert/map/timeline_bar_book_num.html")
