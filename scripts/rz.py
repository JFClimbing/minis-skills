#!/usr/bin/env python3
"""压图工具 —— 跨平台图片压缩（Windows / macOS / Linux / Minis）

用法：
  python3 rz.py <文件名或路径> [...]
  python3 rz.py --all-known          # 压缩名单里所有已存在的文件
  python3 rz.py --check <名称...>     # 只看大小，不改
  python3 rz.py --dir <目录路径>       # 指定工作目录

说明：
  自动检测平台和附件目录。已小于 400KB 的自动跳过。
  同一个文件重复压不会变差。
"""
import os
import sys
import platform

try:
    from PIL import Image
except ImportError:
    print("❌ 缺少 Pillow 库。请安装：pip install Pillow")
    print("   或: pip3 install Pillow")
    sys.exit(1)

# ─── Platform detection & default paths ─────────────────────────────
def get_default_upload_dir():
    """根据当前操作系统返回默认上传目录"""
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Linux":
        # Minis/iSH 环境
        if os.path.isdir("/var/minis"):
            return "/var/minis/attachments/uploads"
        # WSL / 普通 Linux
        return os.path.join(home, ".minis", "attachments", "uploads")

    elif system == "Darwin":  # macOS
        return os.path.join(home, ".minis", "attachments", "uploads")

    elif system == "Windows":
        # 优先使用 APPDATA，回退到用户目录
        appdata = os.environ.get("APPDATA", home)
        return os.path.join(home, ".minis", "attachments", "uploads")

    else:
        return os.path.join(home, ".minis", "attachments", "uploads")


DEFAULT_DIR = get_default_upload_dir()
MAX_PX = 1200
SKIP_BELOW = 400 * 1024  # 已经很小了就不动

# 历史名单（--all-known 时用）
KNOWN = [
    "photo_06550D0B", "photo_C9C2C2CF", "photo_CF55BFB5", "photo_9DD88B8B",
    "photo_666BCC8C", "photo_C2A1D110", "photo_D89E20EF", "photo_DD7F6CC1",
    "photo_34EF7B1F", "photo_EDFFBE6C", "photo_A5D6C486", "photo_CC9767CE",
    "photo_DCCEE1F8", "photo_5E624093", "photo_BB696DEC", "photo_D43A0158",
    "photo_AFBE4B5F", "photo_CE65AD10", "photo_CB0B9ECC", "photo_DE9C52F6",
    "photo_DC3C4751", "photo_89A80389", "photo_9D8B7B04", "photo_9419CDFC",
    "photo_1CE1A069",
]


def resolve(name, work_dir=None):
    """返回实际存在的路径（支持给名字不带扩展名）"""
    base_dir = work_dir or DEFAULT_DIR

    # 绝对路径直接检查
    if os.path.isabs(name) and os.path.exists(name):
        return name

    # 相对路径：先检查当前目录，再检查工作目录
    for cand in (name, os.path.join(base_dir, name)):
        if os.path.exists(cand):
            return cand

    # 尝试补扩展名
    base = os.path.splitext(os.path.basename(name))[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".heic", ".avif",
                ".JPG", ".JPEG", ".PNG", ".WEBP", ".HEIC", ".AVIF"):
        for d in (".", base_dir):
            p = os.path.join(d, base + ext)
            if os.path.exists(p):
                return p
    return None


def format_size(size_bytes):
    """人类可读的文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.0f} KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f} MB"


def compress(p):
    """压缩单张图片，返回 (原始大小, 新大小, 状态)"""
    s0 = os.path.getsize(p)
    if s0 < SKIP_BELOW:
        return s0, s0, "skip"

    try:
        im = Image.open(p)
    except Exception as e:
        return s0, s0, f"error: {e}"

    # RGBA/P 模式转 RGB（JPEG 不支持透明通道）
    if im.mode in ("RGBA", "P", "LA", "PA"):
        im = im.convert("RGB")

    # 缩放
    w, h = im.size
    if max(w, h) > MAX_PX:
        r = MAX_PX / max(w, h)
        im = im.resize((max(1, int(w * r)), max(1, int(h * r))), Image.LANCZOS)

    # 保存为 JPEG
    newp = os.path.splitext(p)[0] + ".jpg"
    im.save(newp, "JPEG", quality=72, optimize=True)

    # 如果新文件更小，替换原文件
    if newp != p and os.path.exists(newp) and os.path.getsize(newp) < s0:
        os.remove(p)

    s1 = os.path.getsize(newp)
    return s0, s1, "ok"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    # 解析 --dir 参数
    work_dir = None
    if "--dir" in args:
        idx = args.index("--dir")
        if idx + 1 < len(args):
            work_dir = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
            if not os.path.isdir(work_dir):
                print(f"  ✗ 目录不存在: {work_dir}")
                return 1
        else:
            print("  ✗ --dir 需要一个目录参数")
            return 1

    check_only = "--check" in args
    args = [a for a in args if a != "--check"]

    if args and args[0] == "--all-known":
        targets = []
        for n in KNOWN:
            p = resolve(n, work_dir)
            if p:
                targets.append(p)
    else:
        targets = []
        for a in args:
            p = resolve(a, work_dir)
            if p:
                targets.append(p)
            else:
                print(f"  ✗ 找不到: {a}")

    if not targets:
        print("没有可处理的文件")
        return 1

    # 显示平台信息
    system = platform.system()
    print(f"💻 平台: {system} | 工作目录: {work_dir or DEFAULT_DIR}")

    b = a_ = 0
    rows = []
    for p in targets:
        try:
            if check_only:
                s = os.path.getsize(p)
                b += s
                rows.append((os.path.basename(p), s, s, "check"))
                continue
            s0, s1, st = compress(p)
            b += s0
            a_ += s1
            rows.append((os.path.basename(p), s0, s1, st))
        except Exception as e:
            print(f"  ✗ {os.path.basename(p)}: {e}")

    if not check_only:
        saved = b - a_
        pct = 100 * (1 - a_ / max(b, 1))
        print(f"处理 {len(rows)} 个文件：{format_size(b)} → {format_size(a_)}（省 {pct:.0f}%）\n")

    for n, s0, s1, st in sorted(rows, key=lambda x: -x[1]):
        tag = "（已小，跳过）" if st == "skip" else ""
        if st.startswith("error"):
            tag = f"（{st}）"
        print(f"  {format_size(s0):>10} → {format_size(s1):>10}  {n} {tag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
