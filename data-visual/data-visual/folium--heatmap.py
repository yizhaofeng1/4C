import folium
from folium.plugins import HeatMap
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


# 定义分类函数
def classify_region(region):
    # 检查是否为中国省份
    for province in china_provinces:
        if province in region:
            return province

    # 如果地区包含"省"或"县"等字样但未匹配到具体省份，归类为"其他中国地区"
    if '省' in region or '县' in region or '市' in region:
        return '地理区域'

    # 默认忽略其他非中国地区或未知地区
    return None


# 应用分类函数
df['分类'] = df['province_group'].apply(classify_region)

# 过滤掉分类为 None 的行
df = df[df['分类'].notnull()]

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

# 创建地图，中心位置为中国
m = folium.Map(location=[35, 105], zoom_start=4)

# 准备热力图数据
heat_data = [[item[1][1], item[1][0], item[1][2]] for item in final_result]

# 添加热力图层
HeatMap(heat_data, radius=15, blur=10, max_zoom=1,tiles='Stamen Toner').add_to(m)

# 保存地图为HTML文件
m.save("./insert/map/china_heatmap.html")

print("热力图已生成并保存为 china_heatmap.html")