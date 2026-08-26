# 贡献指南 | Contributing Guide

感谢你对 **兽临其境** 项目的关注！虽然本项目已不再由原作者积极维护，但非常欢迎社区贡献者参与改进和扩展。

## 🌟 如何贡献

### 报告问题

如果你在使用过程中发现 Bug 或有功能建议，请在 [Issues](https://github.com/yizhaofeng1/4C/issues) 中提交，并尽可能提供以下信息：

- 问题的详细描述
- 复现步骤
- 你的运行环境（OS、Python 版本、浏览器等）
- 相关截图或日志

### 提交代码

1. **Fork** 本仓库
2. 创建你的 Feature 分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m 'feat: add some feature'`
4. 推送到远程：`git push origin feature/your-feature-name`
5. 创建 **Pull Request**

### Commit 规范

建议使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

| 前缀 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加旅游景点推荐功能` |
| `fix` | Bug 修复 | `fix: 修复地图渲染异常` |
| `docs` | 文档更新 | `docs: 更新部署指南` |
| `style` | 代码格式调整 | `style: 统一缩进风格` |
| `refactor` | 代码重构 | `refactor: 重构视图函数` |
| `perf` | 性能优化 | `perf: 优化地图加载速度` |

## 🎯 推荐贡献方向

以下是原作者留下的几个值得探索的方向（详见 README）：

1. **🌟 地图 × 旅游业融合** — 将神兽分布与旅游景点信息结合
2. **📚 数据扩展** — 接入更多古籍文献数据
3. **⚛️ 前端升级** — 迁移至 React / Vue 框架
4. **🐳 容器化部署** — Docker + K8s 方案
5. **📱 移动端适配** — 小程序或移动端 App

## 🔧 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/yizhaofeng1/4C.git
cd 4C

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
cd web/myproject
python manage.py migrate
python manage.py runserver
```

## 📄 许可证

贡献的代码将同样遵循 [MIT License](LICENSE)。
