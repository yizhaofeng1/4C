import csv
import hashlib
import json
import os
import re
import time

import json5
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from tqdm import tqdm

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 初始化Deepseek客户端
client = OpenAI(
    base_url="https://api.deepseek.com/",
    api_key="your_key"  # 请替换为实际API密钥
)

# ================== 全局配置 ==================
# CSV文件字段定义
REQUIRED_FIELDS = [
    "name", "appearance", "original_habitat", "modern_location",
    "source_excerpt", "source_translation", "abilities", "symbolism",
    "category", "mountain_location", "chapter"
]

# 缓存文件路径
CACHE_PATH = current_dir+"\\location_cache.json"
SYMBOL_CACHE_PATH = current_dir+ "\\symbol_cache.json"

# 分块处理参数
CHUNK_SIZE = 1000  # 文本分块大小（建议800-1200）
REQUEST_INTERVAL = 3  # 分块请求间隔（秒）

# 省份白名单
PROVINCE_WHITELIST = {
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省",
    "福建省", "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省", "海南省",
    "四川省", "贵州省", "云南省", "陕西省", "甘肃省", "青海省", "台湾省", "北京市",
    "天津市", "上海市", "重庆市", "内蒙古自治区", "广西壮族自治区", "西藏自治区",
    "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区"
}
# 新增分类映射配置
CATEGORY_MAPPING = {
    "兽类": ["状如", "兽", "虎", "豹", "熊", "彘", "牛", "马"],
    "鸟类": ["鸟", "禽", "翼", "羽", "凤", "凰", "鹊"],
    "鱼类与水生生物": ["鱼", "蛟", "龙", "鳖", "鼍", "水", "海"],
    "爬行与蛇类": ["蛇", "虺", "蜥", "蜴", "蟒"],
    "混合形态或超自然生物": ["人面", "龙首", "神", "鬼", "九尾", "三足"]
}
CHAPTER_KEYWORDS = {
    "山经": ["南山经", "西山经", "北山经", "东山经", "中山经"],
    "海外经": ["海外南", "海外西", "海外北", "海外东"],
    "海内经": ["海内南", "海内西", "海内北", "海内东"],
    "大荒经": ["大荒东", "大荒南", "大荒西", "大荒北"]
}
# ================== 提示词模板 ==================
SYSTEM_PROMPT = f"""
请严格按以下要求处理《山海经》文本：
1. 识别并提取所有异兽/神怪信息
2. 生成包含以下字段的JSON对象：
{{
  "name": "名称（必填）",
  "appearance": "外貌特征（50字内）",
  "original_habitat": "山海经中所写的地理位置（一般后面带山字，结合名称信息网上搜索确认一下,以网上搜索出来的位置为准）",
  "modern_location": "现代对应位置（未知填'未知'，可以结合名称信息再搜索推断一下）",
  "source_excerpt": "原文节选（保留关键特征）",
  "source_translation": "白话文翻译（30字内）",
  "abilities": "特殊能力（中文分号分隔）",
  "symbolism": "象征意义（20字内）",
  "category": "科属分类（兽类/鸟类/鱼类与水生生物/爬行与蛇类/混合形态或超自然生物），通过名称结合网上信息查找",
  "mountain_location": "所处方位（南/西/北/东/中），如果未知就通过名称在网上信息查找",
  "chapter": "所处章节（山经/海内经/大荒经/海外经），如果未知就通过名称在网上信息查找"
}}
3. 最终以JSON数组形式输出
4. 确保字段值均用双引号包裹
"""

GEO_PROMPT = """
根据《山海经》地理描述或是异兽的名称来推断现代位置：
1. 优先使用以下对应关系：
   昆仑山 -> 青海省
   不周山 -> 山西省/帕米尔高原
   青丘山 -> 山东省
   赤水 -> 金沙江流域（四川省/云南省）
2. 其他情况按以下优先级判断：
   (1) 山脉现代同名位置
   (2) 古代地名对照表
   (3) 方位推测
   (4)谐音或是同音词对应的推测的山
3. 返回标准省份全称（多个用中文分号分隔）
"""

# 修改象征意义提示词
SYMBOL_PROMPT = """
分析异兽象征意义：
1. 使用2-3个简短词语描述（不超过4个汉字）
2. 用中文分号分隔
3. 示例：
   输入：其状如牛，赤身人面 -> 战争预警;母性崇拜
   输入：御火食铁 -> 兵戈之象;金火之精
4. 无明确象征时返回"未知"
"""

classic_mapping_set = {
            "昆仑": "青海省",
            "不周山": "山西省;新疆维吾尔自治区",
            "青丘国": "山东省",
            "赤水": "四川省;云南省",
            "中山": "河南省",
            "招揪之山": "广西省",
            "青丘山": "山东省",
            "招播山": "广西省",
            "要阳之山": "广东省;江西省;湖南省",
            "首阳山": "河南省",
            "阳华之山": "陕西省",
            "箕尾之山": "湖南省；江西省",
            "敖岸之山": "河南省"
        }

# ================== 初始化缓存 ==================
def load_cache(file_path):
    """加载缓存文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"初始化新缓存：{file_path}")
        return {}


LOCATION_CACHE = load_cache(CACHE_PATH)
SYMBOL_CACHE = load_cache(SYMBOL_CACHE_PATH)


# ================== 核心功能 ==================
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)
def api_request(content, prompt_type):
    """带重试机制的API请求"""
    messages = [
        {"role": "system",
         "content": SYSTEM_PROMPT if prompt_type == "main" else GEO_PROMPT if prompt_type == "geo" else SYMBOL_PROMPT},
        {"role": "user", "content": content}
    ]
    return client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        timeout=60
    )


def clean_text(text):
    """文本预处理"""
    text = re.sub(r'【.*?】|\d|\[.*?\]|（.*?）|\(.*?\)', '', text)
    return re.sub(r'[\n\s]+', ' ', text).strip()


def extract_json(response):
    """增强型JSON解析"""
    try:
        # 统一引号处理
        cleaned = (
            response.replace("‘", "'").replace("’", "'")
            .replace("“", '"').replace("”", '"')
            .replace("\\n", "")
        )

        # 自动平衡括号
        open_cnt = cleaned.count('[') + cleaned.count('{')
        close_cnt = cleaned.count(']') + cleaned.count('}')
        if open_cnt > close_cnt:
            cleaned += ']' * (open_cnt - close_cnt)

        # 提取JSON内容
        if match := re.search(r'\[.*\]', cleaned, re.DOTALL):
            return json5.loads(match.group())
        return []
    except Exception as e:
        print(f"JSON解析失败：{str(e)}")
        return []


def process_location(text: str) -> str:
    """
    处理地理位置查询，包含经典对应关系和严格校验
    参数：
        text: 包含异兽名称和原文位置的查询文本
    返回：
        标准化后的省份名称字符串（多个用中文分号分隔）
    """
    # 生成缓存键
    cache_key = hashlib.md5(text.encode("utf-8")).hexdigest()

    # 检查缓存
    if cache_key in LOCATION_CACHE:
        return LOCATION_CACHE[cache_key]

    try:
        # API请求（带重试机制）
        response = api_request(text, "geo").choices[0].message.content
        raw = response.strip("。、")

        # 经典地理位置强制对应（优先处理）
        classic_mapping =classic_mapping_set
        for key, value in classic_mapping.items():
            if key in text:
                LOCATION_CACHE[cache_key] = value
                return value

        # 增强版省份提取
        province_pattern = r"""
        (北京市|天津市|上海市|重庆市|
        河北省|山西省|辽宁省|吉林省|黑龙江省|江苏省|浙江省|安徽省|福建省|江西省|山东省|河南省|
        湖北省|湖南省|广东省|海南省|四川省|贵州省|云南省|陕西省|甘肃省|青海省|台湾省|
        内蒙古自治区|广西壮族自治区|西藏自治区|宁夏回族自治区|新疆维吾尔自治区|
        香港特别行政区|澳门特别行政区|太平洋|日本|北美|大西洋)
        """

        locations = []
        # 处理多种分隔符
        for loc in re.split(r'[;；，、,/]', raw):
            # 清理括号内容
            clean_loc = re.sub(r"[（(].*?[)）]", "", loc).strip()
            # 严格匹配省份
            if match := re.search(province_pattern, clean_loc, re.X):
                valid_loc = match.group(1)
                if valid_loc in PROVINCE_WHITELIST:
                    locations.append(valid_loc)

        # 方位词兜底逻辑
        if not locations:
            direction_mapping = {
                "东": ["山东省", "江苏省"],
                "南": ["广东省", "广西壮族自治区"],
                "西": ["山西省", "陕西省"],
                "北": ["河北省", "辽宁省"]
            }
            for direction, provinces in direction_mapping.items():
                if direction in raw:
                    locations.extend(provinces)

        # 结果处理
        locations = list(dict.fromkeys(locations))  # 去重保留顺序
        result = "；".join(locations[:3]) if locations else "未知"  # 最多返回3个

        # 更新缓存
        LOCATION_CACHE[cache_key] = result
        with open(CACHE_PATH, "a", encoding="utf-8") as f:
            json.dump({cache_key: result}, f, ensure_ascii=False)
            f.write("\n")

        return result

    except Exception as e:
        print(f"地理位置查询失败：{str(e)}")
        return "未知"


def process_symbolism(item: dict) -> str:
    """
    处理象征意义查询，严格限制输出格式
    参数：
        item: 包含异兽信息的字典
    返回：
        标准化后的象征意义字符串（2-3个词语，用中文分号分隔）
    """
    # 生成缓存键
    cache_key = hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest()

    # 检查缓存
    if cache_key in SYMBOL_CACHE:
        return SYMBOL_CACHE[cache_key]

    try:
        # 构造查询内容
        query = "\n".join([
            f"名称：{item.get('name', '')}",
            f"外貌：{item.get('appearance', '')}",
            f"能力：{item.get('abilities', '')}",
            f"原文：{item.get('source_excerpt', '')[:100]}"  # 截取前100字防止过长
        ])

        # API请求
        response = api_request(query, "symbol").choices[0].message.content

        # 严格清洗结果
        symbols = re.sub(r"[^;\u4e00-\u9fa5]", "", response)  # 移除非中文和分号
        symbols = symbols.strip(";")

        # 拆分和过滤
        symbol_list = []
        for s in symbols.split(";"):
            clean_s = s.strip()
            # 长度限制：2-4个汉字
            if 2 <= len(clean_s) <= 4:
                symbol_list.append(clean_s)
            # 特殊处理常见长词
            elif len(clean_s) > 4:
                for word in re.findall(r"..?..?", clean_s):
                    symbol_list.append(word)

        # 最终处理
        symbol_list = list(dict.fromkeys(symbol_list))  # 去重
        symbols = "；".join(symbol_list[:3])  # 最多3个

        # 空值处理
        result = symbols if symbols else "未知"

        # 更新缓存
        SYMBOL_CACHE[cache_key] = result
        with open(SYMBOL_CACHE_PATH, "a", encoding="utf-8") as f:
            json.dump({cache_key: result}, f, ensure_ascii=False)
            f.write("\n")

        return result

    except Exception as e:
        print(f"象征意义查询失败：{str(e)}")
        return "未知"
# ================== 新增处理函数 ==================
def determine_category(appearance: str) -> str:
    """智能判断科属分类"""
    for category, keywords in CATEGORY_MAPPING.items():
        for kw in keywords:
            if kw in appearance:
                return category
    return "混合形态或超自然生物"


def extract_mountain_location(habitat: str) -> str:
    """提取山体方位"""
    direction_map = {
        "南": ["南", "赤"],
        "西": ["西", "白"],
        "北": ["北", "黑"],
        "东": ["东", "青"],
        "中": ["中", "黄"]
    }
    for direction, keywords in direction_map.items():
        for kw in keywords:
            if kw in habitat:
                return direction
    return "未知"
def determine_chapter(source_excerpt: str) -> str:
    """判断所属章节"""
    for chapter, keywords in CHAPTER_KEYWORDS.items():
        for kw in keywords:
            if kw in source_excerpt:
                return chapter
    # 模糊匹配
    if "大荒" in source_excerpt:
        return "大荒经"
    if "海外" in source_excerpt:
        return "海外经"
    if "海内" in source_excerpt:
        return "海内经"
    return "未知"
# ================== 主流程 ==================
def main():
    # 读取原始文本
    with open(current_dir+"\\山海经全译.txt", "r", encoding="utf-8") as f:
        raw_text = clean_text(f.read())

    # 分块处理
    text_chunks = [raw_text[i:i + CHUNK_SIZE] for i in range(0, len(raw_text), CHUNK_SIZE)]

    # 结果写入CSV,增添使用a,从x个模块开始，则为text_chunks[x:],start=x
    with open(current_dir+"\\shanhaijin.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()

        for idx, chunk in enumerate(tqdm(text_chunks[368:], desc="处理进度"),start=368):
            try:
                # 请求间隔控制
                if idx > 368:
                    time.sleep(REQUEST_INTERVAL)

                # API调用
                response = api_request(chunk, "main")
                data = extract_json(response.choices[0].message.content)

                # 处理每个条目
                for item in data:
                    # 填充默认值
                    item.setdefault("modern_location", "未知")
                    item.setdefault("symbolism", "未知")
                    item.setdefault("source_translation", "暂无翻译")
                    item.setdefault("category", determine_category(item.get("appearance", "")))
                    # 山体方位
                    if "mountain_location" not in item or item["mountain_location"] == "未知":
                        item["mountain_location"] = extract_mountain_location(item.get("original_habitat", ""))
                    # 处理地理位置
                    if item["original_habitat"] and item["modern_location"] == "未知":
                        item["modern_location"] = process_location(
                            f"名称：{item['name']}\n位置：{item['original_habitat']}"
                        )
                        # 章节判断
                    if "chapter" not in item or item["chapter"] == "未知":
                        item["chapter"] = determine_chapter(item.get("source_excerpt", ""))
                        # 字段验证
                        item["category"] = item["category"] if item["category"] in CATEGORY_MAPPING.keys() else "未知"
                        item["mountain_location"] = item["mountain_location"] if item["mountain_location"] in ["南","西","北","东","中"] else "未知"
                        item["chapter"] = item["chapter"] if item["chapter"] in CHAPTER_KEYWORDS.keys() else "未知"

                    # 处理象征意义
                    if item["symbolism"] in ["未知", ""]:
                        item["symbolism"] = process_symbolism(item)

                    writer.writerow(item)

            except Exception as e:
                print(f"\n分块处理失败：{str(e)}")
                with open("error_chunks.log", "a") as f:
                    f.write(f"\n失败分块索引：{idx}\n内容片段：{chunk[:200]}...\n")

    # 最终保存缓存
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(LOCATION_CACHE, f, ensure_ascii=False)
    with open(SYMBOL_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(SYMBOL_CACHE, f, ensure_ascii=False)
    print("处理完成！缓存已保存")


if __name__ == "__main__":
    main()
    file_path=current_dir+"\\shanhaijin.csv"
