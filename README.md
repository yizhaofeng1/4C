<p align="center">
  <img src="https://img.shields.io/badge/Award-🏆_National_3rd_Prize-gold?style=for-the-badge" alt="Award Badge"/>
  <img src="https://img.shields.io/badge/Competition-中国大学生计算机设计大赛-blue?style=for-the-badge" alt="Competition Badge"/>
  <img src="https://img.shields.io/badge/Track-数据可视化-green?style=for-the-badge" alt="Track Badge"/>
</p>

<h1 align="center">🐉 兽临其境 — 山海经生物地理信息系统与文献编年可视化</h1>

<p align="center">
  <strong>Shanhaijing Creature Geographic Information System & Literature Chronological Visualization</strong>
</p>

<p align="center">
  <a href="#-项目简介">简介</a> •
  <a href="#-功能特性">功能</a> •
  <a href="#️-技术架构">架构</a> •
  <a href="#-快速开始">部署</a> •
  <a href="#-目录结构">目录</a> •
  <a href="#-未来展望">展望</a> •
  <a href="#-license">License</a>
</p>

---

## 📖 项目简介

**兽临其境** 是第17届 **中国大学生计算机设计大赛** 数据可视化赛道 **国家三等奖** 获奖作品。

本项目以中国古代经典文献《山海经》为研究对象，利用 **DeepSeek 大语言模型 API** 对《山海经全译》（约 30.5 万字）进行自动化文本抽取与实体识别，提取出神兽名称、形态描述、栖息地、象征意义、所属篇章等结构化数据，并将其中的地理信息映射到中国现实省份，最终在 Web 端以多种可视化图表与交互式地图的形式呈现。

> **English**: *"Beast in the Realm"* is a data visualization project that maps mythical creatures from *"Shanhaijing" (Classic of Mountains and Seas)* — one of China's oldest mythological geography texts — to real Chinese provinces. The project uses the DeepSeek LLM API to automatically extract structured data from ~305,000 characters of classical Chinese text, and visualizes the geographical distribution of mythical creatures through interactive maps and charts built with Django + PyEcharts.

### 🎯 核心价值

- **文化数字化**：将两千多年前的古籍以现代数据可视化方式重新诠释
- **AI 赋能古籍研究**：利用大语言模型 API 自动化处理大规模古文本
- **地理信息可视化**：将神话生物的分布映射到真实的中国地理版图

## ✨ 功能特性

### 🗺️ 交互式地图
- **2D 中国地图**：展示各省份神兽分布数量，支持鼠标悬停查看详情
- **3D 地球仪**：全球视角呈现《山海经》神兽分布的立体效果
- **热力图**：以热力形式直观展示神兽密度分布
- **时序地图**：按《山海经》篇章顺序动态展示分布变化

### 📊 数据可视化图表
- **柱状图 / 3D 柱状图**：各省份神兽数量对比
- **饼图 / 玫瑰图**：神兽类别占比分析
- **树形图**：《山海经》篇章 → 类别 → 神兽名称的层级结构
- **雷达图**：多维度数据对比分析
- **词云图**：以凤凰造型展示高频关键词
- **水球图**：数据比例可视化
- **情感分析可视化**：象征意义的情感倾向分析

### 🔍 异兽查询系统
- 支持按名称搜索《山海经》中的异兽
- 查询结果包含：形态描述、栖息地、现代对应地点、原文摘录、白话翻译、能力、象征意义等
- 集成 **Stable Diffusion** 模型，根据异兽描述自动生成 AI 绘图

### 📚 文献价值展示
- 象征意义分析页面：揭示古人对异兽创作的趋向
- 学术价值页面：文献贡献与学科演进的可视化分析
- 资料分析页面：异兽数据的系统性解读

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端展示层                          │
│  Bootstrap 5 · Font Awesome · ECharts · PyEcharts       │
│  交互式地图 · 数据图表 · 视频背景 · 响应式布局            │
├─────────────────────────────────────────────────────────┤
│                    Django 后端服务                        │
│  Views (页面路由) · API (异兽查询) · Template Engine      │
├─────────────────────────────────────────────────────────┤
│                      数据层                              │
│  MySQL / SQLite · CSV 数据文件                            │
├─────────────────────────────────────────────────────────┤
│                  数据预处理 Pipeline                      │
│  DeepSeek API (文本抽取) · Pandas (数据清洗)              │
│  OpenAI SDK (API 调用) · 自动化实体识别                   │
├─────────────────────────────────────────────────────────┤
│                   AI 图像生成                             │
│  Stable Diffusion v1.5 · Diffusers · PyTorch             │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **前端** | HTML5 / CSS3 / JavaScript | 页面结构与交互 |
| **UI 框架** | Bootstrap 5 / Font Awesome | 响应式布局与图标 |
| **可视化** | PyEcharts / ECharts | 图表与地图渲染 |
| **后端** | Django 4.2 | Web 服务框架 |
| **数据库** | MySQL / SQLite | 结构化数据存储 |
| **数据处理** | Pandas / Python | 数据清洗与预处理 |
| **LLM** | DeepSeek API | 古文本自动化抽取 |
| **AI 绘图** | Stable Diffusion / Diffusers | 异兽图像生成 |
| **深度学习** | PyTorch | 模型推理 |

## 🚀 快速开始

### 环境要求

- Python >= 3.9
- pip
- MySQL（可选，默认使用 CSV 数据文件）
- CUDA GPU（可选，用于 Stable Diffusion 图像生成加速）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yizhaofeng1/4C.git
cd 4C

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 启动项目

```bash
# 进入 Django 项目目录
cd web/myproject

# 数据库迁移（首次运行）
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

浏览器访问 **http://127.0.0.1:8000/** 即可看到项目首页。

### ⚠️ 注意事项

1. **API Key**：`database/` 目录下的数据预处理脚本需要配置 DeepSeek API Key，本仓库不提供密钥，请自行申请并替换。
2. **Stable Diffusion**：异兽查询功能中的 AI 绘图需要下载 `runwayml/stable-diffusion-v1-5` 模型（约 4GB），首次运行会自动下载。若无 GPU，运行速度较慢。
3. **数据文件**：项目已内置预处理完成的 CSV 数据文件（`database/database/shanhaijin.csv`），可直接使用而无需重新运行数据抽取流程。
4. **地图资源**：地图文件使用 [echarts-countries-js](https://github.com/echarts-maps/echarts-countries-js) 提供的中国地图数据。

## 📁 目录结构

```
4C/
├── database/                          # 数据预处理模块
│   └── database/
│       ├── deepseak-api.py            # DeepSeek API 调用 - 山海经文本抽取
│       ├── SQL.py                     # MySQL 数据库写入脚本
│       ├── data clean.py             # 数据清洗脚本
│       ├── shanhaijin.csv            # 预处理完成的结构化数据（440+ 条记录）
│       ├── 山海经.txt                 # 山海经原文文本
│       ├── 山海经全译.txt              # 山海经全译文本（~30.5 万字）
│       ├── location_cache.json       # 地理位置缓存
│       ├── symbol_cache.json         # 象征意义缓存
│       └── error_chunks.log          # 错误日志
│
├── data-visual/                       # 数据可视化脚本模块
│   └── data-visual/
│       ├── 3D Map--2D Heat.py        # 3D 地图与 2D 热力图
│       ├── Bar 3D.py                 # 3D 柱状图
│       ├── Bar.py                    # 柱状图
│       ├── Line.py                   # 折线图
│       ├── Pie.py                    # 饼图
│       ├── Mutiple Pie.py            # 多层饼图
│       ├── Radar.py                  # 雷达图
│       ├── Tree.py                   # 树形图
│       ├── Liquid.py                 # 水球图
│       ├── Global Map.py             # 全球地图
│       ├── Global Map2.py            # 全球地图 v2
│       ├── sklearn Bar.py            # sklearn 分析柱状图
│       ├── text_cloud.py             # 词云生成
│       ├── Fix.py                    # 数据修复脚本
│       ├── folium--heatmap.py        # Folium 热力图
│       ├── Map/                      # 地图相关资源
│       └── insert/                   # 生成的 HTML 可视化文件
│
├── web/                               # Django Web 项目
│   └── myproject/
│       ├── manage.py                 # Django 管理脚本
│       ├── myproject/                # Django 项目配置
│       │   ├── settings.py           # 项目设置
│       │   ├── urls.py               # 根 URL 配置
│       │   ├── wsgi.py               # WSGI 入口
│       │   └── asgi.py               # ASGI 入口
│       ├── myapp/                    # Django 应用
│       │   ├── views.py              # 视图函数（页面路由 + 查询 API）
│       │   ├── urls.py               # 应用 URL 配置
│       │   ├── models.py             # 数据库模型定义
│       │   └── static/               # 静态资源（CSS/JS/图片/视频）
│       └── templates/                # HTML 模板
│           ├── index.html            # 首页
│           ├── search.html           # 异兽查询页面
│           └── html/
│               ├── sitePage/         # 功能页面（象征意义/学术价值/地图/分析）
│               ├── Map/              # 3D 地图页面
│               └── insert/           # 嵌入式可视化图表页面
│                   ├── 3D/           # 3D 可视化
│                   ├── map/          # 地图可视化
│                   ├── symbol/       # 象征分析可视化
│                   ├── data-visual-analysis/  # 数据分析可视化
│                   └── value-visualization/   # 价值可视化
│
├── 设计与开发文档/                     # 项目文档
│   ├── 开发文档.pdf                   # 完整开发文档（需求分析/架构/实现/部署）
│   └── requirements.txt              # 依赖列表（备份）
│
├── requirements.txt                   # Python 依赖列表
├── .gitignore                         # Git 忽略规则
├── LICENSE                            # MIT 许可证
├── CONTRIBUTING.md                    # 贡献指南
└── README.md                          # 本文件
```

## 📊 数据处理流程

```mermaid
graph LR
    A[山海经全译.txt<br/>~30.5 万字] --> B[DeepSeek API<br/>文本分块抽取]
    B --> C[实体识别<br/>名称/形态/栖息地/能力...]
    C --> D[数据清洗<br/>Pandas]
    D --> E[地理映射<br/>古地名→现代省份]
    E --> F[shanhaijin.csv<br/>结构化数据]
    F --> G[MySQL 数据库]
    F --> H[PyEcharts 可视化]
    H --> I[交互式地图/图表]
```

**数据字段说明**：

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `name` | 神兽名称 | 九尾狐 |
| `appearance` | 形态描述 | 其状如狐而九尾 |
| `original_habitat` | 原始栖息地（古文记载） | 青丘之山 |
| `modern_location` | 对应现代地理位置 | 山东省 |
| `source_excerpt` | 原文摘录 | 有兽焉，其状如狐而九尾... |
| `source_translation` | 白话翻译 | 有一种野兽，形状像狐狸却有九条尾巴... |
| `abilities` | 能力描述 | 能食人 |
| `symbolism` | 象征意义 | 祥瑞、子孙繁衍 |
| `category` | 分类 | 兽 |
| `mountain_location` | 方位（东/西/南/北/中） | 东 |
| `chapter` | 所属篇章 | 南山经 |

## 🔮 未来展望

> ⚠️ 本项目已停止维护，以下为作者构想的进一步完善方向，欢迎感兴趣的开发者参考并推进：

### 🌟 地图分布 × 旅游业融合（核心构想）

这是本项目最初未能实现的重要设想：**将《山海经》神兽地理分布与旅游业网站结合**。具体可以考虑：

- 将神兽分布地图与该省份的文化旅游景点信息关联，提供"追寻山海经足迹"的文化旅行路线推荐
- 结合景区 API（如携程、高德地图 POI），自动推荐与神兽栖息地相近的景点
- 设计"山海经主题文化游"路线规划功能
- 接入天气、交通等实时数据，提供完整的旅行辅助信息

### 其他可扩展方向

- **数据扩展**：接入更多古籍文献（如《搜神记》《博物志》），丰富异兽数据库
- **前端升级**：将 Vanilla JS 迁移至 React / Vue，提升可维护性
- **云端部署**：使用 Docker + Kubernetes 进行容器化部署，提供在线演示
- **移动端适配**：开发小程序或移动端 App
- **社区互动**：添加用户评论、收藏、分享功能

如果你对上述方向感兴趣，非常欢迎通过 [Issues](https://github.com/yizhaofeng1/4C/issues) 或 [Pull Requests](https://github.com/yizhaofeng1/4C/pulls) 提出改进方案！

## 📎 相关资源

- 📖 [山海经 - 国家图书馆](http://shj.nlc.cn/) — 项目"了解更多"链接指向的在线资源
- 🗺️ [echarts-countries-js](https://github.com/echarts-maps/echarts-countries-js) — 地图数据来源
- 🤖 [DeepSeek](https://www.deepseek.com/) — 文本抽取所用大语言模型
- 📊 [PyEcharts](https://pyecharts.org/) — 数据可视化库

## 📝 开发文档

完整的项目设计与开发文档请查阅 **`设计与开发文档/开发文档.pdf`**，包含：

- 项目背景与需求分析
- 系统整体架构设计
- 数据抽取与预处理流程详解
- 前端交互设计说明
- 数据库结构设计
- 部署与运行指南

## 📄 License

本项目采用 [MIT License](LICENSE) 开源。

## 🙏 致谢

- 感谢 **中国大学生计算机设计大赛** 组委会提供的比赛平台
- 感谢所有帮助我完成此作品的老师与同学
- 感谢 [DeepSeek](https://www.deepseek.com/)、[PyEcharts](https://pyecharts.org/)、[ECharts](https://echarts.apache.org/) 等优秀的开源项目
- 感谢中华古典文献《山海经》为本项目提供的深厚文化底蕴

---

<p align="center">
  <sub>Made with ❤️ for the 17th Chinese College Student Computer Design Competition</sub>
</p>
