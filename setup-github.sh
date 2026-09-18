#!/bin/bash
# GitHub Repository Setup Script for Minis Skills
# This script helps you push the skills to GitHub

set -e

echo "🚀 GitHub Repository Setup for Minis Skills"
echo ""

# Check if git is configured
if [ -z "$(git config --global user.email)" ] || [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Git user not configured. Please run:"
    echo ""
    echo "  git config --global user.email 'your-email@example.com'"
    echo "  git config --global user.name 'Your Name'"
    echo ""
    exit 1
fi

# Check if repository exists
echo "📋 Steps to create GitHub repository:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Repository name: minis-skills"
echo "3. Description: Skills collection for Minis AI assistant"
echo "4. Make it Public (for open source)"
echo "5. Do NOT initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""

read -p "Have you created the repository? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please create the repository first, then run this script again."
    exit 1
fi

# Get repository URL
read -p "Enter your GitHub username: " GITHUB_USERNAME
REPO_URL="https://github.com/${GITHUB_USERNAME}/minis-skills.git"

echo ""
echo "📤 Pushing to GitHub..."
echo "Repository URL: ${REPO_URL}"
echo ""

# Add remote and push
cd /tmp/minis-skills
git remote add origin "${REPO_URL}" 2>/dev/null || git remote set-url origin "${REPO_URL}"
git branch -M main
git push -u origin main

echo ""
echo "✅ Success! Your repository is now live at:"
echo "   https://github.com/${GITHUB_USERNAME}/minis-skills"
echo ""
echo "📋 Next steps:"
echo "1. Share this link with others:"
echo "   https://github.com/${GITHUB_USERNAME}/minis-skills"
echo ""
echo "2. Others can install with one command:"
echo "   curl -sSL https://raw.githubusercontent.com/${GITHUB_USERNAME}/minis-skills/main/install.sh | bash"
echo ""
echo "3. Or clone manually:"
echo "   git clone https://github.com/${GITHUB_USERNAME}/minis-skills.git"
echo ""
echo "📚 Documentation:"
echo "   - README.md: https://github.com/${GITHUB_USERNAME}/minis-skills#readme"
echo "   - Quick Start: https://github.com/${GITHUB_USERNAME}/minis-skills/blob/main/docs/快速开始.md"
echo "   - Setup Guide: https://github.com/${GITHUB_USERNAME}/minis-skills/blob/main/docs/设置指南.md"
echo ""
echo "🎉 Congratulations! You've open-sourced your Minis skills!"
