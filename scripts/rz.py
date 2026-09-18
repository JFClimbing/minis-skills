#!/usr/bin/env python3
"""压图工具 —— 把上传的大图压到 1200px / JPEG q72

用法：
  python3 /root/bin/rz.py <文件名或路径> [...]
  python3 /root/bin/rz.py --all-known          # 压缩名单里所有已存在的文件
  python3 /root/bin/rz.py --check <名称...>     # 只看大小，不改

说明：
  默认在 /var/minis/attachments/uploads 下查找。
  同一个文件重复压不会变差（已小于 400KB 的直接跳过）。
"""
import os
import sys

from PIL import Image

D = "/var/minis/attachments/uploads"
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


def resolve(name):
    """返回实际存在的路径（支持给名字不带扩展名）"""
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for cand in (name, os.path.join(D, name)):
        if os.path.exists(cand):
            return cand
    base = os.path.splitext(os.path.basename(name))[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".heic", ".JPG", ".PNG"):
        p = os.path.join(D, base + ext)
        if os.path.exists(p):
            return p
    return None


def compress(p):
    s0 = os.path.getsize(p)
    if s0 < SKIP_BELOW:
        return s0, s0, "skip"
    im = Image.open(p)
    if im.mode in ("RGBA", "P", "LA"):
        im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > MAX_PX:
        r = MAX_PX / max(w, h)
        im = im.resize((max(1, int(w * r)), max(1, int(h * r))), Image.LANCZOS)
    newp = os.path.splitext(p)[0] + ".jpg"
    im.save(newp, "JPEG", quality=72, optimize=True)
    if newp != p and os.path.exists(newp) and os.path.getsize(newp) < s0:
        os.remove(p)
    s1 = os.path.getsize(newp)
    return s0, s1, "ok"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    check_only = "--check" in args
    args = [a for a in args if a != "--check"]

    if args and args[0] == "--all-known":
        targets = []
        for n in KNOWN:
            p = resolve(n)
            if p:
                targets.append(p)
    else:
        targets = []
        for a in args:
            p = resolve(a)
            if p:
                targets.append(p)
            else:
                print(f"  ✗ 找不到: {a}")

    if not targets:
        print("没有可处理的文件")
        return 1

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
        print(f"处理 {len(rows)} 个文件：{b/1024/1024:.1f} MB → {a_/1024/1024:.1f} MB"
              f"（省 {100*(1-a_/max(b,1)):.0f}%）\n")
    for n, s0, s1, st in sorted(rows, key=lambda x: -x[1]):
        tag = "（已小，跳过）" if st == "skip" else ""
        print(f"  {s0/1024:8.0f} KB → {s1/1024:6.0f} KB  {n} {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
