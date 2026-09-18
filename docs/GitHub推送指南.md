# GitHub 推送指南

## 快速步骤

### 第一步：创建 GitHub 仓库
1. 打开 https://github.com/new
2. 填写信息：
   - **Repository name**: `minis-skills`
   - **Description**: `Skills collection for Minis AI assistant - 社交媒体登录、图片压缩等技能`
   - **Public** ✓
   - **不要**勾选「Initialize this repository with a README」
3. 点击「Create repository」

### 第二步：配置 Git 身份
在 Minis 终端中运行（替换为你的信息）：
```bash
git config --global user.email "你的邮箱@example.com"
git config --global user.name "你的名字"
```

### 第三步：推送到 GitHub
在 Minis 终端中运行（替换为你的 GitHub 用户名）：
```bash
cd /tmp/minis-skills
./push-to-github.sh 你的GitHub用户名
```

---

## 推送成功后

你的仓库地址：
```
https://github.com/你的用户名/minis-skills
```

分享给朋友的一键安装命令：
```bash
curl -sSL https://raw.githubusercontent.com/你的用户名/minis-skills/main/install.sh | bash
```

---

## 常见问题

### Q: 我没有 GitHub 账号怎么办？
A: 访问 https://github.com/signup 注册一个免费账号。

### Q: 推送时提示权限错误？
A: 可能需要配置 GitHub 认证。最简单的方式：
1. 安装 GitHub CLI: `apk add gh`（如果可用）
2. 或者使用 Personal Access Token：
   - 访问 https://github.com/settings/tokens
   - 生成新 token（勾选 repo 权限）
   - 推送时输入 token 作为密码

### Q: 我想用 SSH 而不是 HTTPS？
A: 生成 SSH 密钥：
```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub
```
然后把公钥添加到 https://github.com/settings/keys

---

## 仓库内容预览

推送成功后，你的仓库会显示：

```
minis-skills/
├── README.md                    # 项目说明（自动显示）
├── LICENSE                      # MIT 开源许可证
├── install.sh                   # 一键安装脚本
├── scripts/
│   └── rz.py                    # 图片压缩工具
├── skills/
│   ├── social-media-login/      # 社交媒体登录技能
│   └── image-compression/       # 图片压缩技能
└── docs/
    ├── 设置指南.md
    ├── 快速开始.md
    └── FAQ.md
```

---

## 后续维护

### 更新仓库
```bash
cd /tmp/minis-skills
# 修改文件后
git add -A
git commit -m "更新说明"
git push
```

### 添加新技能
```bash
# 在 skills/ 目录下创建新技能
mkdir skills/new-skill
# 创建 SKILL.md 文件
# 然后推送
git add -A
git commit -m "添加新技能: new-skill"
git push
```

---

**最后更新**: 2026-09-18
