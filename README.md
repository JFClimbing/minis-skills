# Minis Skills Collection

A collection of skills for [Minis](https://minis.app) and other AI assistants — now with **cross-platform support** for Windows, macOS, Linux, and WSL.

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

Automatically compress uploaded images to avoid hitting conversation size limits.

**Features**:
- Compress images to 1200px / JPEG q72
- Skip already small images (<400KB)
- Session handover file template
- Prevent conversation size issues

**Trigger words**: "压缩图片", "图片太大", "会话超限"

---

## 🖥️ Supported Platforms

| Platform | Status | Install Method |
|----------|--------|---------------|
| **Minis/iSH** (iOS) | ✅ Full Support | `install.sh` or manual |
| **macOS** | ✅ Full Support | `install.sh` or Homebrew |
| **Linux** (Ubuntu/Debian/Fedora/Arch) | ✅ Full Support | `install.sh` or apt/dnf/pacman |
| **Windows** (Git Bash/MSYS2) | ✅ Full Support | `install.sh` or pip |
| **WSL** (Windows Subsystem for Linux) | ✅ Full Support | `install.sh` or apt |

---

## 🚀 Quick Start

### Option A: One-Click Install (All Platforms)

```bash
# Copy and paste this into your terminal:
curl -sSL https://raw.githubusercontent.com/JFClimbing/minis-skills/main/install.sh | bash
```

The script automatically detects your platform and installs everything.

### Option B: Manual Installation

#### Minis/iSH
```bash
# Install dependencies
apk update && apk add python3 py3-pillow git

# Clone and install
cd /var/minis/skills/
git clone https://github.com/JFClimbing/minis-skills.git temp-skills
cp -r temp-skills/skills/* .
mkdir -p /root/bin
cp -r temp-skills/scripts/* /root/bin/
chmod +x /root/bin/rz.py
rm -rf temp-skills
```

#### macOS
```bash
# Install dependencies
brew install python3 pillow git

# Clone and install
mkdir -p ~/.minis/skills ~/.local/bin
git clone https://github.com/JFClimbing/minis-skills.git /tmp/minis-skills
cp -r /tmp/minis-skills/skills/* ~/.minis/skills/
cp /tmp/minis-skills/scripts/rz.py ~/.local/bin/
rm -rf /tmp/minis-skills
```

#### Linux (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-pil git

# Clone and install
mkdir -p ~/.minis/skills ~/.local/bin
git clone https://github.com/JFClimbing/minis-skills.git /tmp/minis-skills
cp -r /tmp/minis-skills/skills/* ~/.minis/skills/
cp /tmp/minis-skills/scripts/rz.py ~/.local/bin/
rm -rf /tmp/minis-skills
```

#### Windows (Git Bash / MSYS2)
```bash
# Install Python dependencies
pip install Pillow requests

# Clone and install
mkdir -p ~/.minis/skills ~/.local/bin
git clone https://github.com/JFClimbing/minis-skills.git /tmp/minis-skills
cp -r /tmp/minis-skills/skills/* ~/.minis/skills/
cp /tmp/minis-skills/scripts/rz.py ~/.local/bin/
rm -rf /tmp/minis-skills
```

#### Windows (PowerShell)
```powershell
# Install Python dependencies
pip install Pillow requests

# Clone and install
New-Item -ItemType Directory -Path "$env:USERPROFILE\.minis\skills", "$env:USERPROFILE\.local\bin" -Force
git clone https://github.com/JFClimbing/minis-skills.git "$env:TEMP\minis-skills"
Copy-Item -Recurse "$env:TEMP\minis-skills\skills\*" "$env:USERPROFILE\.minis\skills\"
Copy-Item "$env:TEMP\minis-skills\scripts\rz.py" "$env:USERPROFILE\.local\bin\"
Remove-Item -Recurse "$env:TEMP\minis-skills"
```

### Step 2: Configure AI Model
Open Minis → Settings → Model Providers → Add your API Key (OpenAI / Anthropic / Gemini)

### Step 3: Test Installation
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
# Compress all known images
python3 ~/.local/bin/rz.py --all-known

# Compress specific image
python3 ~/.local/bin/rz.py photo_ABC123

# Check size without compressing
python3 ~/.local/bin/rz.py --check photo_ABC123

# Specify custom directory
python3 ~/.local/bin/rz.py --dir /path/to/images photo_ABC123
```

**Platform-specific paths**:

| Platform | Default Upload Directory |
|----------|------------------------|
| Minis/iSH | `/var/minis/attachments/uploads` |
| macOS | `~/.minis/attachments/uploads` |
| Linux | `~/.minis/attachments/uploads` |
| Windows | `~/.minis/attachments/uploads` |
| WSL | `~/.minis/attachments/uploads` |

---

## 📁 Repository Structure

```
minis-skills/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── install.sh                         # Cross-platform install script
├── scripts/
│   └── rz.py                          # Cross-platform image compression tool
└── skills/
    ├── social-media-login/
    │   └── SKILL.md                   # Cross-platform social media login skill
    └── image-compression/
        └── SKILL.md                   # Cross-platform image compression skill
```

---

## ⚠️ Limitations

1. **Verification codes**: Cannot be bypassed - you must manually enter verification codes and complete face recognition
2. **Login expiration**: Douyin login expires in ~hours, Xiaohongshu in ~days
3. **API Key required**: You need your own OpenAI/Anthropic/Gemini API key
4. **Image limits**: Control number of images sent to avoid conversation size limits
5. **Platform-specific browser automation**: Minis uses `minis-browser-use`, other platforms use Playwright/Selenium

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

- **Issues**: [GitHub Issues](https://github.com/JFClimbing/minis-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JFClimbing/minis-skills/discussions)
- **Minis Community**: Ask in Minis conversation

---

**Last Updated**: 2026-09-18
**Version**: 1.1.0 (Cross-Platform Update)
