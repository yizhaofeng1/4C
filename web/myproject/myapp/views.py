import logging
import csv
import os
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
# from .models import Shj
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO
import base64
from openai import OpenAI

logger = logging.getLogger(__name__)
def index(request):
    return render(request, 'index.html')



def china_map_3D(request):
    return render(request, 'html/Map/china_map_3D.html')
def combined_map_globe(request):
    return render(request, 'html/insert/3D/combined_map_globe.html')
def time_varying_map_globe(request):
    return render(request, 'html/insert/3D/time_varying_map_globe.html')
def category_counts_pie_chart(request):
    return render(request, 'html/insert/data-visual-analysis/category_counts_pie_chart.html')
def liquid_shape_diamond(request):
    return render(request, 'html/insert/data-visual-analysis/liquid_shape_diamond.html')
def combined_charts_new(request):
    return render(request, 'html/insert/data-visual-analysis/combined_charts_new.html')
def strange_creatures_rose_chart(request):
    return render(request, 'html/insert/data-visual-analysis/strange_creatures_rose_chart.html')
def tree_shanhaijin_category_name(request):
    return render(request, 'html/insert/data-visual-analysis/tree_shanhaijin_category_name.html')
def china_map_2D(request):
    return render(request, 'html/insert/map/china_map_2D.html')
def china_heatmap(request):
    return render(request, 'html/insert/map/china_heatmap.html')
def direction_statistics_3d_bar(request):
    return render(request, 'html/insert/map/direction_statistics_3d_bar.html')
def Genus(request):
    return render(request, 'html/insert/map/Genus.html')
def province_quantity_bar_chart(request):
    return render(request, 'html/insert/map/province_quantity_bar_chart.html')
def province_quantity_horizontal_pictorialbar(request):
    return render(request, 'html/insert/map/province_quantity_horizontal_pictorialbar.html')
def scriptures(request):
    return render(request, 'html/insert/map/scriptures.html')
def timeline_bar_book_num(request):
    return render(request, 'html/insert/map/timeline_bar_book_num.html')
def symbolism_sentiment_analysis(request):
    return render(request, 'html/insert/symbol/symbolism_sentiment_analysis.html')
def wordcloud_phoenix_custom(request):
    return render(request, 'html/insert/symbol/wordcloud_phoenix_custom.html')
def combined_charts(request):
    return render(request, 'html/insert/value-visualization/combined_charts.html')
def wordcloud_phoenix_custom(request):
    return render(request, 'html/insert/value-visualization/wordcloud_phoenix_custom.html')



def search(request):
    return render(request, 'html/search.html')
def site1(request):
    return render(request, 'html/sitePage/site1.html')
def site2(request):
    return render(request, 'html/sitePage/site2.html')
def site3(request):
    return render(request, 'html/sitePage/site3.html')
def site4(request):
    return render(request, 'html/sitePage/site4.html')
def map1(request):
    return render(request, 'html/sitePage/地图1.html')
def map2(request):
    return render(request, 'html/sitePage/地图2.html')
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 获取当前文件（views.py）所在的目录
current_dir = Path(__file__).parent

# 构建模型的绝对路径
# 假设模型路径相对于 views.py 文件的相对位置
# 你需要根据实际情况调整相对路径
# model_relative_path = Path("diffusers-main/diffusers/stable-diffusion-v1-5")
# model_path = current_dir / model_relative_path
# 构建模型目录的绝对路径
# 全局加载 StableDiffusionPipeline
# model_id = "runwayml/stable-diffusion-v1-5"  # 这里可以根据需要替换为其他diffusers模型的ID
# pipe = StableDiffusionPipeline.from_pretrained(model_id)
# pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def get_creature_by_name(request):
    logger.info('Received request to get creature by name')
    logger.info('Request GET parameters: %s', request.GET)
    name = request.GET.get('name')

    if not name:
        logger.warning('Missing name parameter in request')
        return JsonResponse({'error': '缺少name参数'}, status=400)

    # 注释掉数据库查询部分（如要使用请删除注释部分）
    # try:
    #     # 从数据库中查询生物
    #     creature = Shj.objects.get(name__iexact=name.strip())
    #     logger.info('Found creature: %s', creature.name)
    #     data = {
    #         'name': creature.name,
    #         'appearance': creature.appearance if creature.appearance else '',
    #         'original_habitat': creature.original_habitat if creature.original_habitat else '',
    #         'modern_location': creature.modern_location if creature.modern_location else '',
    #         'source_excerpt': creature.source_excerpt if creature.source_excerpt else '',
    #         'source_translation': creature.source_translation if creature.source_translation else '',
    #         'abilities': creature.abilities if creature.abilities else '',
    #         'symbolism': creature.symbolism if creature.symbolism else '',
    #         'category': creature.category if creature.category else '',
    #         'mountain_location': creature.mountain_location if creature.mountain_location else '',
    #         'chapter': creature.chapter if creature.chapter else ''
    #     }
    # except Shj.DoesNotExist:
    #     logger.warning('Creature with name %s not found in database', name)
    #     data = None
    # except Exception as e:
    #     logger.error('An error occurred while querying the database: %s', e)
    #     logger.info('Falling back to CSV file query.')
    #     data = None

    # 直接从 CSV 文件查询
    file_path = '../../database/shanhaijin.csv'
    data = None
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                csv_name = row.get('name', '').strip().lower()
                if csv_name == name.strip().lower():
                    logger.info('Found creature: %s in CSV file', csv_name)
                    data = {
                        'name': row.get('name', '').strip(),
                        'appearance': row.get('appearance', '').strip(),
                        'original_habitat': row.get('original_habitat', '').strip(),
                        'modern_location': row.get('modern_location', '').strip(),
                        'source_excerpt': row.get('source_excerpt', '').strip(),
                        'source_translation': row.get('source_translation', '').strip(),
                        'abilities': row.get('abilities', '').strip(),
                        'symbolism': row.get('symbolism', '').strip(),
                        'category': row.get('category', '').strip(),
                        'mountain_location': row.get('mountain_location', '').strip(),
                        'chapter': row.get('chapter', '').strip(),
                    }
                    break
        if data is None:
            logger.warning('Creature with name %s not found in CSV file', name)
            return JsonResponse({'error': '未找到对应的生物'}, status=404)
    except FileNotFoundError:
        logger.error('CSV file not found at path: %s', file_path)
        return JsonResponse({'error': '未找到'}, status=500)
    except Exception as e:
        logger.error('An error occurred while querying the CSV file: %s', e)
        return JsonResponse({'error': '查询 CSV 文件出错'}, status=500)

    # 生成图像
    prompt = f"{data['name']} {data['source_translation']} {data['abilities']} {data['symbolism']}"
    api_key = 'sk-929383ac40cf4bdfa60560ccaba19282'
    client = OpenAI(
        base_url="https://api.deepseek.com/",
        api_key=api_key
    )
    # 调用 API 进行翻译
    response = client.chat.completions.create(
        model="deepseek-chat",  # 指定使用的 DeepSeek 模型
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的翻译助手，仅输出翻译后的英文内容，不包含其他额外信息。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # 提取翻译后的内容并更新 prompt 变量
    model_id = "runwayml/stable-diffusion-v1-5"  # 这里可以根据需要替换为其他diffusers模型的ID
    pipe = StableDiffusionPipeline.from_pretrained(model_id,safety_checker=None)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    prompt = response.choices[0].message.content
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    data['image'] = image_data
    return JsonResponse(data)