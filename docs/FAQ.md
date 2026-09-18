# Frequently Asked Questions (FAQ)

## Installation

### Q: How do I install Minis?
A: Search for "Minis" in the App Store and download it. It requires iOS 16.0 or later.

### Q: Do I need to pay for Minis?
A: Minis is free to download. You need your own AI model API key (OpenAI, Anthropic, or Gemini).

### Q: Can I use this on Android?
A: Currently, Minis only supports iOS. Android users can try Termux with similar tools.

---

## Skills

### Q: Why don't I see the skills after installation?
A: Check if the skills are in `/var/minis/skills/` directory. Each skill should have a `SKILL.md` file.

### Q: How do I update the skills?
A: Run the install script again, or manually pull the latest version from GitHub:
```bash
cd /var/minis/skills/
git clone https://github.com/your-username/minis-skills.git temp-skills
cp -r temp-skills/skills/* .
rm -rf temp-skills
```

### Q: Can I create my own skills?
A: Yes! See the [skill-creator](https://github.com/your-username/minis-skills/blob/main/skills/skill-creator/SKILL.md) skill for guidance.

---

## Social Media Login

### Q: Why can't the AI bypass verification codes?
A: Verification codes and face recognition are security measures that require human interaction. This is a limitation of the platforms, not the tool.

### Q: How long does the login session last?
A: Douyin login expires in about 2-3 hours. Xiaohongshu login lasts about 1-2 days.

### Q: Can I login to multiple accounts?
A: Yes, but you need to logout and login again for each account.

### Q: Why can't I see my post images?
A: Douyin images require waiting 10 seconds for lazy loading. Xiaohongshu images need xsec_token which is only available in the creator center.

---

## Image Compression

### Q: Why do I need to compress images?
A: Minis has a 32MB conversation size limit. Each image you send adds to this limit. Compressing images helps you stay within the limit.

### Q: Will compressing images reduce quality?
A: The compression tool reduces images to 1200px and JPEG quality 72. This is usually sufficient for most purposes while significantly reducing file size.

### Q: Can I compress images that are already in the conversation?
A: No, once images are in the conversation history, they cannot be compressed. You need to start a new conversation.

### Q: How do I check the conversation size?
A: Use `minis-sessions-cli status` to check the current session size.

---

## Configuration

### Q: How do I add my API key?
A: Go to Settings → Model Providers in Minis, and add your API key for OpenAI, Anthropic, or Gemini.

### Q: Which AI model should I use?
A: We recommend Claude 3.5 Sonnet or GPT-4o for the best experience. For image generation, you can add DALL-E 3 or Gemini.

### Q: How do I set environment variables?
A: Go to Settings → Environment Variables in Minis. You can add variables like `DOUYIN_PHONE` and `XHS_PHONE` for easier login.

---

## Troubleshooting

### Q: The script says "not running in Minis/iSH"
A: Make sure you're running the script in the Minis app's terminal, not in a regular terminal.

### Q: Python is not found
A: Install Python: `apk add python3`

### Q: Pillow is not found
A: Install Pillow: `apk add py3-pillow`

### Q: Git clone fails
A: Check your internet connection. If behind a firewall, try using HTTPS instead of SSH.

### Q: Skills are not triggering
A: Make sure you're using the correct trigger words. Check the SKILL.md files for the exact trigger words.

---

## Advanced Usage

### Q: Can I use this for commercial purposes?
A: Yes, this project is licensed under MIT License. You can use it for personal or commercial purposes.

### Q: How do I contribute to this project?
A: Fork the repository, make your changes, and submit a Pull Request. See the Contributing section in README.md.

### Q: Can I add my own skills?
A: Yes! Create a new folder in `skills/` with a `SKILL.md` file. See the skill-creator skill for guidance.

### Q: How do I backup my skills?
A: Copy the `/var/minis/skills/` directory to a safe location. You can also use Git to version control your skills.

---

## Support

### Q: Where can I get help?
A: 
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Minis Community**: Ask in Minis conversation

### Q: How do I report a bug?
A: Open an issue on GitHub with:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Screenshots (if applicable)

### Q: How do I request a feature?
A: Open an issue on GitHub with:
1. Feature description
2. Use case
3. Expected behavior

---

**Last Updated**: 2026-09-18
