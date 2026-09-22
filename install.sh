#!/bin/bash
# Minis Skills Installation Script — Cross-Platform
# Usage: curl -sSL https://raw.githubusercontent.com/JFClimbing/minis-skills/main/install.sh | bash
#
# Supported: Minis/iSH, macOS, Linux, Windows (Git Bash/MSYS2/WSL)

set -e

echo "🧩 Installing Minis Skills..."
echo ""

# ─── Detect platform ───────────────────────────────────────────────
detect_platform() {
    case "$(uname -s)" in
        Linux*)
            if [ -d "/var/minis" ]; then
                echo "minis"
            elif grep -qi microsoft /proc/version 2>/dev/null; then
                echo "wsl"
            else
                echo "linux"
            fi
            ;;
        Darwin*)  echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *)        echo "unknown" ;;
    esac
}

PLATFORM=$(detect_platform)
echo "📋 Detected platform: $PLATFORM"

# ─── Set paths per platform ────────────────────────────────────────
set_paths() {
    case "$PLATFORM" in
        minis)
            SKILLS_DIR="/var/minis/skills"
            BIN_DIR="/root/bin"
            ATTACHMENTS_DIR="/var/minis/attachments/uploads"
            PYTHON="python3"
            ;;
        wsl)
            SKILLS_DIR="$HOME/.minis/skills"
            BIN_DIR="$HOME/.local/bin"
            ATTACHMENTS_DIR="$HOME/.minis/attachments/uploads"
            PYTHON="python3"
            ;;
        linux)
            SKILLS_DIR="$HOME/.minis/skills"
            BIN_DIR="$HOME/.local/bin"
            ATTACHMENTS_DIR="$HOME/.minis/attachments/uploads"
            PYTHON="python3"
            ;;
        macos)
            SKILLS_DIR="$HOME/.minis/skills"
            BIN_DIR="$HOME/.local/bin"
            ATTACHMENTS_DIR="$HOME/.minis/attachments/uploads"
            PYTHON="python3"
            ;;
        windows)
            # Prefer python3, fall back to python
            if command -v python3 &>/dev/null; then
                PYTHON="python3"
            elif command -v python &>/dev/null; then
                PYTHON="python"
            else
                echo "❌ Python 3 is required but not found."
                echo "   Install from https://www.python.org/downloads/"
                exit 1
            fi
            SKILLS_DIR="$HOME/.minis/skills"
            BIN_DIR="$HOME/.local/bin"
            ATTACHMENTS_DIR="$HOME/.minis/attachments/uploads"
            ;;
        *)
            echo "❌ Unsupported platform: $(uname -s)"
            echo "   Supported: Minis/iSH, macOS, Linux, Windows (Git Bash/MSYS2/WSL)"
            exit 1
            ;;
    esac
}

set_paths

# ─── Install dependencies ──────────────────────────────────────────
install_deps() {
    echo "📦 Installing dependencies..."
    case "$PLATFORM" in
        minis)
            apk update && apk add python3 py3-pillow git
            ;;
        linux)
            if command -v apt-get &>/dev/null; then
                sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-pil git
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y python3 python3-pip python3-pillow git
            elif command -v pacman &>/dev/null; then
                sudo pacman -S --noconfirm python python-pip python-pillow git
            elif command -v apk &>/dev/null; then
                apk update && apk add python3 py3-pillow git
            else
                echo "⚠️  Could not detect package manager. Install manually: python3, pillow, git"
            fi
            ;;
        macos)
            if command -v brew &>/dev/null; then
                brew install python3 pillow git 2>/dev/null || brew install python3 git
                pip3 install Pillow 2>/dev/null || true
            else
                echo "⚠️  Homebrew not found. Install from https://brew.sh"
                echo "   Then run: brew install python3 pillow git"
            fi
            ;;
        windows)
            if command -v pip &>/dev/null; then
                pip install Pillow requests 2>/dev/null || true
            elif command -v pip3 &>/dev/null; then
                pip3 install Pillow requests 2>/dev/null || true
            else
                echo "⚠️  pip not found. Install Pillow manually:"
                echo "   pip install Pillow requests"
            fi
            ;;
        wsl)
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-pil git
            ;;
    esac
}

install_deps

# ─── Create directories ────────────────────────────────────────────
echo "📁 Creating directories..."
mkdir -p "$SKILLS_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$ATTACHMENTS_DIR"

# ─── Clone & copy skills ──────────────────────────────────────────
REPO_URL="https://github.com/JFClimbing/minis-skills.git"

# Detect git or fallback to downloading a zip
if command -v git &>/dev/null; then
    echo "🔍 Cloning skills repository..."
    TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'minis-skills')
    if ! git clone --depth 1 "$REPO_URL" "$TMPDIR/temp-skills"; then
        echo "❌ 克隆仓库失败，请检查网络或改用 zip 方式安装"
        rm -rf "$TMPDIR"
        exit 1
    fi

    echo "📋 Installing skills..."
    cp -r "$TMPDIR/temp-skills/skills/"* "$SKILLS_DIR/"

    echo "📜 Installing scripts..."
    cp -r "$TMPDIR/temp-skills/scripts/"* "$BIN_DIR/"
    chmod +x "$BIN_DIR/rz.py" 2>/dev/null || true

    echo "🧹 Cleaning up..."
    rm -rf "$TMPDIR"
else
    echo "🔍 Downloading skills (git not available)..."
    TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'minis-skills')

    if command -v curl &>/dev/null; then
        curl -sSL "${REPO_URL%.git}/archive/refs/heads/main.zip" -o "$TMPDIR/skills.zip"
    elif command -v wget &>/dev/null; then
        wget -q "${REPO_URL%.git}/archive/refs/heads/main.zip" -O "$TMPDIR/skills.zip"
    else
        echo "❌ Neither curl nor wget found. Install one and retry."
        exit 1
    fi

    # Unzip (works on macOS, Linux, and Windows with unzip)
    if command -v unzip &>/dev/null; then
        unzip -q "$TMPDIR/skills.zip" -d "$TMPDIR"
    elif command -v tar &>/dev/null; then
        tar -xf "$TMPDIR/skills.zip" -C "$TMPDIR"
    else
        echo "❌ Cannot extract zip. Install unzip or tar."
        exit 1
    fi

    EXTRACTED="$TMPDIR/minis-skills-main"
    cp -r "$EXTRACTED/skills/"* "$SKILLS_DIR/"
    cp -r "$EXTRACTED/scripts/"* "$BIN_DIR/"
    chmod +x "$BIN_DIR/rz.py" 2>/dev/null || true
    rm -rf "$TMPDIR"
fi

# ─── Post-install platform tweaks ──────────────────────────────────
case "$PLATFORM" in
    windows)
        # Create a .bat wrapper for rz.py so it can be called easily
        cat > "$BIN_DIR/rz.bat" << 'BATEOF'
@echo off
python "%~dp0rz.py" %*
BATEOF
        echo "📝 Created rz.bat wrapper for Windows"
        ;;
esac

# ─── Verify ────────────────────────────────────────────────────────
echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Installed skills:"
ls -1 "$SKILLS_DIR" 2>/dev/null
echo ""
echo "📜 Installed scripts:"
ls -1 "$BIN_DIR/rz.py" 2>/dev/null
echo ""

case "$PLATFORM" in
    minis)
        echo "🎉 Next steps:"
        echo "   1. Open Minis app"
        echo "   2. In conversation, say '登录抖音' to test social media login"
        echo "   3. Say '压缩图片' to test image compression"
        echo "   4. Say '查看后台数据' to analyze your content"
        ;;
    *)
        echo "🎉 Next steps:"
        echo "   1. Ensure your AI assistant can access skills at: $SKILLS_DIR"
        echo "   2. Image compression script: $BIN_DIR/rz.py"
        echo "   3. Social media login: see skills/social-media-login/"
        echo ""
        echo "   Note: You may need to configure your AI model API key"
        echo "   in Settings → Model Providers"
        ;;
esac
echo ""
