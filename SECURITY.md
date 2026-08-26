# Security Policy

## ⚠️ API Key 安全提醒

本项目源码中 **不应包含** 任何有效的 API Key 或数据库密码。如果你在代码中发现了暴露的密钥，请注意：

1. **DeepSeek API Key**：项目代码中可能残留了开发阶段的 API Key，这些密钥已失效或已更换。请自行申请并配置你自己的密钥。
2. **数据库密码**：请根据你的本地环境修改 `settings.py` 中的数据库配置。

## 报告安全问题

如果你发现了安全漏洞，请通过 [Issues](https://github.com/yizhaofeng1/4C/issues) 私下联系仓库维护者。

## 最佳实践

- 使用环境变量或 `.env` 文件管理敏感配置
- 不要将 API Key 硬编码在源代码中
- 确保 `.gitignore` 包含了 `.env` 文件
