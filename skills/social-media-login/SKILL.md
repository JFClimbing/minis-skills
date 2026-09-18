---
name: social-media-login
description: 自动登录抖音/小红书创作者中心，抓取后台数据（播放、点赞、评论、收藏、分享、划走率等），用于内容分析和运营决策。触发词：登录抖音、登录小红书、查看后台数据、抓取数据、分析账号。
---

# 社交媒体后台数据抓取

## 核心流程

### 1. 抖音创作者中心

**登录路径**：
1. 打开 `creator.douyin.com/creator-micro/content/manage`
2. 选择「验证码登录」→ 输入手机号 → 等待用户输入验证码
3. 可能需要选择账号（如果有多个）
4. 可能需要人脸识别或扫码验证（需用户手动完成）

**数据抓取**：
- 作品管理列表：滚动 `div[class*='list-scroll']` 收集文本
- 解析字段：播放量、点赞、评论、收藏、转发、划走率、文案展开率、吸粉量
- 全部图片：登录后开 `douyin.com/user/self?showTab=post` 取 `/note/<id>` 链接 → 逐条 `douyin.com/note/<id>`（等10s图片懒加载）→ JS 抓 `img[src*=douyinpic]`

**OCR处理**：
- 封面图在创作者中心是 background-image（class `video-card-cover-*`），不是 `<img>`
- 用 `apple-vision ocr <img> --lang zh-Hans --level accurate`

### 2. 小红书创作者中心

**登录路径**：
1. 打开 `creator.xiaohongshu.com/login`
2. 选择「短信登录」→ 输入手机号+验证码
3. 点击「同意并继续」按钮
4. 进入 `creator.xiaohongshu.com/new/note-manager`

**数据抓取**：
- 列表滚动容器：`div.content`
- 每张卡片：`div.note-card`
- 标题：`.note-card__title`
- 数据：`.note-card__stat`（5个字段：👁观看 · 💬评论 · ♡点赞 · ☆收藏 · ↗分享）

**重要**：
- 短信验证码有时会收不到（第一次失败、第二次成功）
- 页面倒计时在后台会冻结
- 创作中心内部接口不需要 xsec_token
- 图片从 `images_list` 字段获取（1080px）

### 3. 数据导出格式

```json
{
  "platform": "douyin|xiaohongshu",
  "account": "账号名",
  "posts": [
    {
      "id": "笔记ID",
      "title": "标题",
      "type": "normal|video",
      "duration_s": 0,
      "views": 0,
      "likes": 0,
      "comments": 0,
      "collected": 0,
      "shared": 0,
      "scroll_rate": 0.0,
      "expand_rate": 0.0,
      "followers_gained": 0,
      "images": ["url1", "url2"],
      "publish_time": "2024-01-01 00:00:00"
    }
  ]
}
```

### 4. 分析维度

- **播放量趋势**：按时间排序，找高/低峰
- **互动率**：(点赞+评论+收藏+分享) / 播放量
- **内容类型对比**：图文 vs 视频，教学 vs 装备 vs 日常
- **封面分析**：OCR 提取文字，分析字数与播放量相关性
- **发布时间**：不同时段的播放量差异
- **划走率**：哪些内容划走率高，分析原因

## 注意事项

- 登录过程需要用户手动输入验证码、扫码等
- 抖音登录态会过期（约几小时后）
- 小红书笔记正文图片抓取需要 xsec_token（创作中心不提供）
- 公开页 `explore` 若无 token → 走创作中心
- 所有数据落盘到 `samples/<平台>-<账号名>/`

## 常用命令

```bash
# 打开抖音创作者中心
minis-browser-use navigate --url https://creator.douyin.com/creator-micro/content/manage

# 打开小红书创作者中心
minis-browser-use navigate --url https://creator.xiaohongshu.com/login

# OCR 图片
apple-vision ocr <image_path> --lang zh-Hans --level accurate
```
