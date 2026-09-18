---
name: image-compression
description: 自动压缩上传图片，避免会话体积超过32MB限制。支持 Windows / macOS / Linux / Minis。触发词：压缩图片、图片太大、会话超限、32MB、上传失败、对话体积。
---

# 图片压缩技能（跨平台）

## 问题背景

AI 助手会话体积上限约 32MB。每次发消息时，App 会把之前所有消息（含历史图片）一起发给模型。累积大量图片 → 超过上限 → 阻断对话。

**关键结论**：
- 压缩磁盘文件救不了（图片已进对话历史）
- 唯一解法：**新建对话** + **后续图片先压缩再发**
- 影响对话体积的是**发图数量**，不是单图大小

## 支持平台

| 平台 | 附件目录 | 安装方式 |
|------|---------|---------|
| Minis/iSH | `/var/minis/attachments/uploads` | `apk add python3 py3-pillow` |
| macOS | `~/.minis/attachments/uploads` | `brew install python3 pillow` |
| Linux (Ubuntu/Debian) | `~/.minis/attachments/uploads` | `apt install python3 python3-pil` |
| Linux (Fedora) | `~/.minis/attachments/uploads` | `dnf install python3 python3-pillow` |
| Linux (Arch) | `~/.minis/attachments/uploads` | `pacman -S python python-pillow` |
| Windows | `~/.minis/attachments/uploads` | `pip install Pillow` |
| WSL | `~/.minis/attachments/uploads` | `apt install python3 python3-pil` |

## 压缩工具

### 位置
- Minis: `/root/bin/rz.py`
- macOS/Linux: `~/.local/bin/rz.py`
- Windows: `~/.local/bin/rz.py`（或 `~/.local/bin/rz.bat`）

### 用法
```bash
# 压缩单个文件
python3 rz.py <文件名或路径>

# 指定工作目录
python3 rz.py --dir /path/to/images <文件名>

# 压缩所有已知文件
python3 rz.py --all-known

# 只看大小，不改
python3 rz.py --check <名称...>
```

### 参数
- **--dir <目录>**：指定工作目录（不使用默认路径）
- 默认在系统检测到的附件目录下查找
- 最大尺寸：1200px
- 跳过阈值：已小于 400KB 的自动跳过
- 同一文件重复压不会变差

### 自动检测逻辑
脚本根据操作系统自动选择附件目录：
- Minis 环境：`/var/minis/attachments/uploads`
- 其他系统：`~/.minis/attachments/uploads`
- 可通过 `--dir` 参数覆盖

## 工作流程

### 1. 接收图片前
- **提醒用户**：「发图前请先压缩，一次只发2-3张」
- 设计稿：一次 2-3 张，看完再发下批
- 截图：1-2 张
- 不要重复发同一批

### 2. 接收图片后
```bash
# 检查图片大小（macOS/Linux）
ls -lh ~/.minis/attachments/uploads/

# 检查图片大小（Windows PowerShell）
Get-ChildItem "$env:USERPROFILE\.minis\attachments\uploads" | Format-Table Name, @{N='Size';E={"{0:N0} KB" -f ($_.Length/1KB)}}

# 压缩所有大图
python3 ~/.local/bin/rz.py --all-known
```

### 3. 会话即将超限时
- 如果接近 32MB：
  1. 告知用户「会话即将超限，建议新建对话」
  2. 创建会话交接文件（如 `content-lab/运营手册/会话交接.md`）
  3. 建议用户在新会话读交接文件恢复上下文

### 4. 新建对话后
- 读取会话交接文件恢复上下文
- 继续压缩后续图片

## 预防措施

1. **发图前压缩**：用户发送图片前，提醒使用压缩工具
2. **分批发送**：设计稿一次2-3张，截图1-2张
3. **避免重复**：不要重复发同一批图片
4. **定期清理**：清理 uploads 目录中不需要的图片

## 会话交接文件模板

```markdown
# 会话交接文件

## 当前任务
[描述当前正在做什么]

## 已完成工作
[列表]

## 待办事项
[列表]

## 关键上下文
[重要信息]

## 文件位置
[相关文件路径]
```

## 常用命令

### macOS / Linux
```bash
# 检查 uploads 目录大小
du -sh ~/.minis/attachments/uploads/

# 压缩所有已知图片
python3 ~/.local/bin/rz.py --all-known

# 清理不需要的图片
rm ~/.minis/attachments/uploads/<filename>
```

### Windows (PowerShell)
```powershell
# 检查 uploads 目录大小
Get-ChildItem "$env:USERPROFILE\.minis\attachments\uploads" -Recurse | Measure-Object -Property Length -Sum | Select-Object @{N='SizeMB';E={[math]::Round($_.Sum/1MB,1)}}

# 压缩所有已知图片
python "$env:USERPROFILE\.local\bin\rz.py" --all-known

# 清理不需要的图片
Remove-Item "$env:USERPROFILE\.minis\attachments\uploads\<filename>"
```

### Minis/iSH
```bash
# 检查 uploads 目录大小
du -sh /var/minis/attachments/uploads/

# 压缩所有已知图片
python3 /root/bin/rz.py --all-known

# 清理不需要的图片
rm /var/minis/attachments/uploads/<filename>
```
