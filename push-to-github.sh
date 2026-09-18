#!/bin/bash
# Push Minis Skills to GitHub
# Usage: ./push-to-github.sh YOUR_GITHUB_USERNAME

set -e

if [ -z "$1" ]; then
    echo "❌ Usage: ./push-to-github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example: ./push-to-github.sh zhangsan"
    exit 1
fi

GITHUB_USERNAME="$1"
REPO_NAME="minis-skills"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🚀 Pushing Minis Skills to GitHub"
echo "   Username: ${GITHUB_USERNAME}"
echo "   Repository: ${REPO_URL}"
echo ""

# Check if git user is configured
if [ -z "$(git config --global user.email)" ]; then
    echo "⚠️  Git user not configured. Please run these commands first:"
    echo ""
    echo "  git config --global user.email 'your-email@example.com'"
    echo "  git config --global user.name 'Your Name'"
    echo ""
    exit 1
fi

# Navigate to repository
cd /tmp/minis-skills

# Add remote
echo "📡 Adding remote repository..."
git remote add origin "${REPO_URL}" 2>/dev/null || git remote set-url origin "${REPO_URL}"

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Push
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Success! Your repository is now live at:"
echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "📋 Share this link with others:"
echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "🎯 One-line install command for others:"
echo "   curl -sSL https://raw.githubusercontent.com/${GITHUB_USERNAME}/${REPO_NAME}/main/install.sh | bash"
echo ""
echo "📚 Documentation:"
echo "   - README: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}#readme"
echo "   - Quick Start: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/blob/main/docs/快速开始.md"
echo ""
echo "🎉 Congratulations! You've open-sourced your Minis skills!"
