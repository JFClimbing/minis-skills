# PR: 跨平台适配 — 支持 Windows / macOS / Linux / WSL

## 概述

本次 PR 为 minis-skills 项目添加跨平台支持，使工具可以在 Windows、macOS、Linux 和 WSL 环境中运行，不仅限于 Minis/iSH。

## 改动内容

### 1. `install.sh` — 跨平台安装脚本

**新增功能**：
- 自动检测操作系统（Minis/iSH、macOS、Linux、Windows、WSL）
- 根据平台选择合适的包管理器安装依赖（apt、dnf、pacman、brew、pip）
- 自动设置平台对应的目录路径
- Windows 上自动创建 `.bat` 包装脚本
- 支持无 git 环境下的 curl/wget 下载方式

**支持的平台**：
| 平台 | 包管理器 | 依赖安装方式 |
|------|---------|-------------|
| Minis/iSH | apk | `apk add python3 py3-pillow git` |
| macOS | Homebrew | `brew install python3 pillow git` |
| Ubuntu/Debian | apt | `apt install python3 python3-pil git` |
| Fedora | dnf | `dnf install python3 python3-pillow git` |
| Arch | pacman | `pacman -S python python-pillow git` |
| Windows | pip | `pip install Pillow` |
| WSL | apt | `apt install python3 python3-pil git` |

### 2. `scripts/rz.py` — 跨平台图片压缩工具

**改进点**：
- 自动检测操作系统，选择正确的附件目录
- 支持 `--dir` 参数指定自定义工作目录
- 改进的文件大小格式化（B/KB/MB 自动选择）
- 改进的错误处理和用户反馈
- 支持更多图片格式（avif）
- Windows 兼容的路径处理

**平台路径映射**：
```python
# Minis/iSH
/var/minis/attachments/uploads

# macOS / Linux / Windows / WSL
~/.minis/attachments/uploads
```

### 3. `skills/image-compression/SKILL.md` — 跨平台文档

**更新内容**：
- 添加跨平台支持表格
- 添加每个平台的安装说明
- 添加 Windows PowerShell 命令示例
- 添加 macOS/Linux/Minis 分别的常用命令
- 更新工具位置说明

### 4. `skills/social-media-login/SKILL.md` — 跨平台文档

**更新内容**：
- 添加平台支持表格和浏览器工具说明
- 添加 Playwright 跨平台安装指南
- 添加每个平台的特定命令（macOS、Windows、Linux、Minis）
- 添加 OCR 工具的跨平台替代方案
- 添加常见问题解答

## 测试情况

| 平台 | install.sh | rz.py | SKILL.md |
|------|-----------|-------|----------|
| Minis/iSH | ✅ 兼容 | ✅ 兼容 | ✅ 已更新 |
| macOS | ✅ 已测试 | ✅ 已测试 | ✅ 已更新 |
| Ubuntu 22.04 | ✅ 已测试 | ✅ 已测试 | ✅ 已更新 |
| Windows 11 (Git Bash) | ✅ 已测试 | ✅ 已测试 | ✅ 已更新 |
| WSL2 | ✅ 已测试 | ✅ 已测试 | ✅ 已更新 |

## 兼容性说明

- **完全向后兼容**：Minis/iSH 环境的所有原有功能保持不变
- **无破坏性变更**：所有新增功能都是可选的
- **依赖最小化**：核心功能仅依赖 Python 3 + Pillow

## 相关 Issue

（如有相关 Issue 请在此引用）

## 截图/演示

（如有界面变更请附截图）
