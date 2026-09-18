#!/bin/bash
# Minis Skills Installation Script
# Usage: curl -sSL https://raw.githubusercontent.com/your-username/minis-skills/main/install.sh | bash

set -e

echo "🚀 Installing Minis Skills..."
echo ""

# Check if running in Minis/iSH
if [ ! -d "/var/minis" ]; then
    echo "❌ Error: This script must be run in Minis/iSH environment"
    echo "   Please open Minis app and run this script in the terminal"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
apk update
apk add python3 py3-pillow git

# Create directories
echo "📁 Creating directories..."
mkdir -p /var/minis/skills/
mkdir -p /root/bin/

# Clone repository
echo "📥 Cloning skills repository..."
cd /var/minis/skills/
if [ -d "temp-skills" ]; then
    rm -rf temp-skills
fi

git clone https://github.com/your-username/minis-skills.git temp-skills

# Copy skills
echo "📋 Installing skills..."
cp -r temp-skills/skills/* .

# Copy scripts
echo "🔧 Installing scripts..."
cp -r temp-skills/scripts/* /root/bin/
chmod +x /root/bin/rz.py

# Clean up
echo "🧹 Cleaning up..."
rm -rf temp-skills

# Verify installation
echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Installed skills:"
ls -1 /var/minis/skills/
echo ""
echo "📋 Installed scripts:"
ls -1 /root/bin/rz.py
echo ""
echo "🎯 Next steps:"
echo "   1. Open Minis app"
echo "   2. In conversation, say '登录抖音' to test social media login"
echo "   3. Say '压缩图片' to test image compression"
echo "   4. Say '查看后台数据' to analyze your content"
echo ""
echo "📚 For more information, see README.md"
echo ""
echo "⚠️  Note: You need to configure your AI model API key in Settings → Model Providers"
