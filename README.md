# Minis Skills Collection

A collection of skills for [Minis](https://minis.app) - an AI assistant running on iOS with a Linux shell environment.

## 📦 Skills Included

### 1. Social Media Login & Data Analysis
**Location**: `skills/social-media-login/`

Automatically login to Douyin (抖音) and Xiaohongshu (小红书) creator centers, extract backend data (views, likes, comments, shares, scroll rate, etc.), and analyze content performance.

**Features**:
- Auto-login to creator centers
- Extract all post data (views, likes, comments, shares, etc.)
- OCR cover images
- Export data as JSON
- Analysis dimensions: engagement rate, content type comparison, cover analysis, etc.

**Trigger words**: "登录抖音", "查看后台数据", "分析账号"

---

### 2. Image Compression
**Location**: `skills/image-compression/`

Automatically compress uploaded images to avoid hitting Minis's 32MB conversation size limit.

**Features**:
- Compress images to 1200px / JPEG q72
- Skip already small images (<400KB)
- Session handover file template
- Prevent conversation size issues

**Trigger words**: "压缩图片", "图片太大", "会话超限"

---

## 🚀 Quick Start

### Step 1: Install Minis
Download Minis from the [App Store](https://apps.apple.com/app/minis/id6449701234) (requires iOS 16.0+)

### Step 2: Configure AI Model
Open Minis → Settings → Model Providers → Add your API Key (OpenAI / Anthropic / Gemini)

### Step 3: Install Skills

#### Option A: One-liner Install Script
Copy and paste this into Minis terminal:

```bash
# Install dependencies
apk update && apk add python3 py3-pillow git

# Clone skills repository
cd /var/minis/skills/
git clone https://github.com/your-username/minis-skills.git temp-skills

# Copy skills to correct location
cp -r temp-skills/skills/* .
cp -r temp-skills/scripts /root/bin/

# Make scripts executable
chmod +x /root/bin/rz.py

# Clean up
rm -rf temp-skills

echo "✅ Installation complete!"
```

#### Option B: Manual Installation
1. Download or clone this repository
2. Copy `skills/` folders to `/var/minis/skills/`
3. Copy `scripts/rz.py` to `/root/bin/`
4. Install dependencies: `apk add python3 py3-pillow`

### Step 4: Test Installation
In Minis conversation, say:
- "登录抖音" → Opens Douyin creator center
- "压缩图片" → Compresses images
- "查看后台数据" → Extracts and analyzes data

---

## 📖 Detailed Usage

### Social Media Login

```bash
# In Minis conversation:
User: 登录抖音
AI: Opens creator.douyin.com → Waits for you to enter verification code → Extracts data

User: 查看后台数据
AI: Analyzes all posts, shows engagement metrics, content performance, etc.
```

**Data Export Format**:
```json
{
  "platform": "douyin",
  "account": "username",
  "posts": [
    {
      "id": "post_id",
      "title": "title",
      "views": 10000,
      "likes": 500,
      "comments": 100,
      "collected": 50,
      "shared": 25
    }
  ]
}
```

### Image Compression

```bash
# Check image sizes
ls -lh /var/minis/attachments/uploads/

# Compress all known images
python3 /root/bin/rz.py --all-known

# Compress specific image
python3 /root/bin/rz.py photo_ABC123

# Check size without compressing
python3 /root/bin/rz.py --check photo_ABC123
```

---

## 📁 Repository Structure

```
minis-skills/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── install.sh                         # One-click install script
├── scripts/
│   └── rz.py                          # Image compression tool
└── skills/
    ├── social-media-login/
    │   └── SKILL.md                   # Social media login skill
    └── image-compression/
        └── SKILL.md                   # Image compression skill
```

---

## ⚠️ Limitations

1. **Verification codes**: Cannot be bypassed - you must manually enter verification codes and complete face recognition
2. **Login expiration**: Douyin login expires in ~hours, Xiaohongshu in ~days
3. **iOS only**: Minis currently only supports iOS 16.0+
4. **API Key required**: You need your own OpenAI/Anthropic/Gemini API key
5. **Image limits**: Control number of images sent to avoid conversation size limits

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Adding New Skills
1. Create a new folder in `skills/`
2. Add a `SKILL.md` file with proper frontmatter
3. Update this README
4. Submit a PR

### Skill Structure
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name + description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/
    ├── references/
    └── assets/
```

---

## 📚 Documentation

- [Minis 完整设置指南](docs/设置指南.md)
- [快速开始](docs/快速开始.md)
- [常见问题](docs/FAQ.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Minis](https://minis.app) - The AI assistant platform
- [iSH](https://ish.app) - Linux shell for iOS
- All contributors and users

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/minis-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/minis-skills/discussions)
- **Minis Community**: Ask in Minis conversation

---

**Last Updated**: 2026-09-18
**Version**: 1.0.0
