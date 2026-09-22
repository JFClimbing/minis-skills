#!/usr/bin/env python3
"""压图工具 —— 跨平台图片压缩（Windows / macOS / Linux / Minis）

用法：
  python3 rz.py <文件名或路径> [...]
  python3 rz.py --all-known          # 压缩工作目录下所有图片
  python3 rz.py --check <名称...>     # 只看大小，不改
  python3 rz.py --dir <目录路径>       # 指定工作目录

说明：
  自动检测平台和附件目录。已小于 400KB 的自动跳过。
  只有压缩后更小才会替换原图，否则保留原图（不会劣化、不会残留副本）。
"""
import os
import sys
import tempfile
import platform

# Windows 默认控制台编码是 GBK，遇到 emoji 会抛 UnicodeEncodeError 崩溃；
# 统一把 stdout/stderr 转成 UTF-8，保证中文和 emoji 都能正常输出。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

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

    # Windows 及其它系统：统一使用用户目录下的 .minis 附件目录
    return os.path.join(home, ".minis", "attachments", "uploads")


DEFAULT_DIR = get_default_upload_dir()
MAX_PX = 1200
SKIP_BELOW = 400 * 1024  # 已经很小了就不动

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".avif"}


def find_images(directory):
    """列出目录下所有图片文件的绝对路径（按文件名排序）"""
    result = []
    try:
        for name in sorted(os.listdir(directory)):
            if os.path.splitext(name)[1].lower() in IMAGE_EXTS:
                result.append(os.path.join(directory, name))
    except OSError:
        pass
    return result


def is_same_file(a, b):
    """判断两个路径是否指向同一文件（兼容大小写不敏感的文件系统，如 Windows）"""
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


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
    """压缩单张图片，返回 (原始大小, 新大小, 状态)

    状态：ok=已压缩且更小；skip=太小或压缩后未变小（保留原图）；keep=目标文件已存在；error=失败
    """
    s0 = os.path.getsize(p)
    if s0 < SKIP_BELOW:
        return s0, s0, "skip"

    # 立即完整读入并关闭源文件句柄（Windows 上覆盖原文件前必须释放句柄）
    try:
        with Image.open(p) as src:
            im = src.copy()
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

    # 目标路径：统一转为 .jpg（小写）
    newp = os.path.splitext(p)[0] + ".jpg"
    same = is_same_file(newp, p)

    # 如果目标 .jpg 已存在且是另一个文件，避免误覆盖，跳过
    if os.path.exists(newp) and not same:
        return s0, s0, "keep"

    # 先写同目录临时文件，再原子替换，避免写出半截文件
    dirname = os.path.dirname(os.path.abspath(p))
    try:
        fd, tmp = tempfile.mkstemp(suffix=".jpg", prefix=".rz-", dir=dirname)
    except OSError as e:
        return s0, s0, f"error: {e}"

    try:
        with os.fdopen(fd, "wb") as f:
            im.save(f, "JPEG", quality=72, optimize=True)

        s_tmp = os.path.getsize(tmp)
        if s_tmp >= s0:
            # 压缩后没变小：丢弃临时文件，保留原图
            os.remove(tmp)
            return s0, s0, "skip"

        # 更小才替换原图
        os.replace(tmp, newp)
        if not same and os.path.exists(p):
            os.remove(p)
        return s0, s_tmp, "ok"
    except Exception as e:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass
        return s0, s0, f"error: {e}"


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

    # --all-known：扫描工作目录下所有图片
    if "--all-known" in args:
        base = work_dir or DEFAULT_DIR
        targets = find_images(base)
        if not targets:
            print(f"  没有找到图片: {base}")
            return 1
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
        if st == "keep":
            tag = "（目标 .jpg 已存在，跳过）"
        if st.startswith("error"):
            tag = f"（{st}）"
        print(f"  {format_size(s0):>10} → {format_size(s1):>10}  {n} {tag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
