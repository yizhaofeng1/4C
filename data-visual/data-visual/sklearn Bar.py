import pandas as pd
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyecharts import options as opts
from pyecharts.charts import Bar
from collections import Counter
from tqdm import tqdm
import time
import os

# 读取 CSV 文件
data = pd.read_csv(r'../../database/shanhaijin.csv')

client = OpenAI(
    base_url="https://api.deepseek.com/",
    api_key="sk-929383ac40cf4bdfa60560ccaba19282"
)

# 超时和重试配置
REQUEST_TIMEOUT = 20  # 单个请求超时时间增加至20秒
MAX_RETRIES = 3  # 最大重试次数
RETRY_BASE_DELAY = 3  # 指数退避基础延迟
MAX_WORKERS = 5  # 并发线程数（根据API限制调整）

# 记录文件路径
RECORD_FILE = 'processed_records.txt'


# 定义带指数退避的请求函数
def get_sentiment_with_retry(text):
    retries = 0
    while retries <= MAX_RETRIES:
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": f"请判断以下文本的情感倾向（好、坏、中性），只需回复一个字：{text}"
                }],
                timeout=REQUEST_TIMEOUT
            )
            sentiment = response.choices[0].message.content.strip().lower()
            return "好" if "好" in sentiment else "坏" if "坏" in sentiment else "中性"
        except Exception as e:
            if retries == MAX_RETRIES:
                print(f"最后失败: {text[:20]}... 错误: {str(e)}")
                return "未知"
            delay = RETRY_BASE_DELAY * (2 ** retries)
            time.sleep(delay)
            retries += 1
    return "未知"


# 进度追踪和断点续传
def process_data(data):
    start_index = 0
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'r') as f:
            try:
                start_index = int(f.read().strip())
            except ValueError:
                pass

    sentiments = data.get('sentiment', pd.Series([None] * len(data))).tolist()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i in range(start_index, len(data)):
            text = data['symbolism'][i]
            futures.append(executor.submit(get_sentiment_with_retry, text))

        with tqdm(total=len(futures), desc="情感分析进度") as pbar:
            for idx, future in enumerate(as_completed(futures), start_index):
                try:
                    sentiments[idx] = future.result()
                except Exception as e:
                    sentiments[idx] = "未知"
                finally:
                    # 每10条保存一次进度
                    if idx % 10 == 0:
                        with open(RECORD_FILE, 'w') as f:
                            f.write(str(idx + 1))
                    pbar.update(1)

    return sentiments


# 主处理流程
if 'sentiment' not in data.columns:
    data['sentiment'] = None

data['sentiment'] = process_data(data)

# 清理记录文件
if os.path.exists(RECORD_FILE):
    os.remove(RECORD_FILE)

# 统计情感倾向数量
sentiment_counter = Counter(data['sentiment'])
required_sentiments = list(sentiment_counter.keys())
sorted_counts = list(sentiment_counter.values())

# 使用 pyecharts 绘制柱状图
bar = (
    Bar(init_opts=opts.InitOpts(bg_color="transparent"))
    .add_xaxis(required_sentiments)
    .add_yaxis("数量", sorted_counts)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="象征意义情感倾向分布"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="情感倾向"),
        yaxis_opts=opts.AxisOpts(name="数量"),
        legend_opts=opts.LegendOpts(is_show=False),
        graphic_opts=[opts.GraphicGroup(
            graphic_item=opts.GraphicItem(left="center", top="center"),
            children=[opts.GraphicRect(
                graphic_item=opts.GraphicItem(z=-10),
                graphic_shape_opts=opts.GraphicShapeOpts(width=100, height=100),
                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="rgba(0,0,0,0)")
            )]
        )]
    )
)

# 渲染图表到 HTML 文件
bar.render("./insert/symbol/symbolism_sentiment_analysis.html")
