#!/usr/bin/env python3
"""Generate hero images for Hugo posts that lack a feature_image."""

import hashlib
import os
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "post"
STATIC_IMAGES = REPO_ROOT / "static" / "images"

WIDTH, HEIGHT = 1200, 630

PALETTES = [
    ((25, 25, 112), (0, 51, 102)),
    ((0, 100, 100), (0, 60, 60)),
    ((80, 40, 120), (40, 20, 80)),
    ((150, 40, 40), (80, 20, 20)),
    ((20, 80, 60), (10, 50, 35)),
    ((40, 60, 120), (20, 30, 80)),
    ((120, 60, 20), (70, 35, 10)),
    ((60, 60, 80), (30, 30, 50)),
    ((0, 80, 120), (0, 40, 70)),
    ((100, 40, 80), (55, 20, 45)),
    ((30, 90, 90), (15, 55, 55)),
    ((90, 70, 30), (55, 40, 15)),
]


def pick_palette(title: str) -> tuple:
    h = int(hashlib.md5(title.encode()).hexdigest(), 16)
    return PALETTES[h % len(PALETTES)]


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_gradient(draw: ImageDraw.Draw, c1, c2):
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = lerp_color(c1, c2, t)
        draw.line([(0, y), (WIDTH, y)], fill=color)


def draw_geometric_accent(draw: ImageDraw.Draw, title: str, c1, c2):
    h = int(hashlib.md5(title.encode()).hexdigest()[:8], 16)
    accent_color = lerp_color(c1, c2, 0.3)
    accent = tuple(min(c + 30, 255) for c in accent_color) + (40,)

    for i in range(3):
        seed = (h >> (i * 8)) & 0xFF
        cx = int((seed / 255) * WIDTH * 0.8)
        cy = int(((h >> (i * 4)) & 0xFF) / 255 * HEIGHT)
        r = 60 + (seed % 120)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)

    for i in range(5):
        seed = (h >> (i * 3)) & 0x1FF
        x_start = seed % WIDTH
        draw.line(
            [(x_start, 0), (x_start - 200, HEIGHT)],
            fill=accent,
            width=2,
        )


def get_font(size: int) -> ImageFont.FreeTypeFont:
    for name in [
        "Ubuntu-Bold.ttf",
        "Ubuntu-Medium.ttf",
        "DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf",
    ]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    for d in ["/usr/share/fonts", "/usr/local/share/fonts"]:
        for root, _, files in os.walk(d):
            for f in files:
                if "Bold" in f and f.endswith(".ttf"):
                    try:
                        return ImageFont.truetype(os.path.join(root, f), size)
                    except OSError:
                        continue
    return ImageFont.load_default()


def wrap_title(title: str, max_chars: int = 30) -> list[str]:
    words = title.split()
    lines: list[str] = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines if lines else [title]


def generate_image(title: str, output_path: Path):
    c1, c2 = pick_palette(title)
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    draw_gradient(draw, c1, c2)
    draw_geometric_accent(draw, title, c1, c2)

    for y in range(HEIGHT // 3, HEIGHT):
        t = (y - HEIGHT // 3) / (HEIGHT * 2 // 3)
        alpha = int(t * 160)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

    font_size = 52
    lines = wrap_title(title, max_chars=32)
    if len(lines) > 3:
        font_size = 40
        lines = wrap_title(title, max_chars=40)
    if len(lines) > 4:
        font_size = 34
        lines = wrap_title(title, max_chars=48)

    font = get_font(font_size)
    small_font = get_font(18)

    line_height = font_size + 12
    total_text_height = len(lines) * line_height
    y_start = HEIGHT - total_text_height - 80

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2
        y = y_start + i * line_height
        draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 180), font=font)
        draw.text((x, y), line, fill=(255, 255, 255, 240), font=font)

    draw.text((40, 30), "cicoria.com", fill=(255, 255, 255, 120), font=small_font)

    accent_bright = tuple(min(c + 80, 255) for c in lerp_color(c1, c2, 0.5))
    line_y = y_start - 20
    draw.line(
        [(WIDTH // 4, line_y), (WIDTH * 3 // 4, line_y)],
        fill=accent_bright + (150,),
        width=2,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, "JPEG", quality=85)


def parse_front_matter(text: str) -> dict:
    result = {}
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return result
    fm = match.group(1)
    for line in fm.splitlines():
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            val = line.split(":", 1)[1].strip()
            result[key] = val
    return result


def get_date_parts(fm: dict) -> tuple[str, str]:
    date_str = fm.get("date", "")
    m = re.match(r"(\d{4})-(\d{2})", date_str)
    if m:
        return m.group(1), m.group(2)
    return "generated", "hero"


def add_feature_image_to_front_matter(text: str, image_path: str) -> str:
    match = re.match(r"^(---\n)(.*?)(\n---)", text, re.DOTALL)
    if not match:
        return text
    pre, fm_body, post = match.group(1), match.group(2), match.group(3)
    new_fm = f'{fm_body}\nfeature_image: "{image_path}"'
    return pre + new_fm + post + text[match.end():]


def main():
    updated = 0
    skipped = 0
    errors: list[tuple[str, str]] = []

    for post_dir in sorted(CONTENT_DIR.iterdir()):
        index_md = post_dir / "index.md"
        if not index_md.is_file():
            continue

        text = index_md.read_text(encoding="utf-8")
        fm = parse_front_matter(text)

        if "feature_image" in fm:
            continue

        title = fm.get("title", post_dir.name).strip('"').strip("'")
        slug = fm.get("slug", post_dir.name).strip('"').strip("'")
        year, month = get_date_parts(fm)

        safe_slug = re.sub(r"[^a-z0-9-]", "", slug.lower())[:60]
        if not safe_slug:
            safe_slug = re.sub(r"[^a-z0-9-]", "", post_dir.name.lower())[:60]

        img_rel = f"/images/{year}/{month}/{safe_slug}-hero.jpg"
        img_abs = STATIC_IMAGES / year / month / f"{safe_slug}-hero.jpg"

        if img_abs.exists():
            skipped += 1
            continue

        try:
            generate_image(title, img_abs)
            new_text = add_feature_image_to_front_matter(text, img_rel)
            index_md.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"  ✓ {post_dir.name}")
        except Exception as e:
            errors.append((post_dir.name, str(e)))
            print(f"  ✗ {post_dir.name}: {e}")

    print(f"\nDone: {updated} generated, {skipped} skipped, {len(errors)} errors")
    if errors:
        for name, err in errors:
            print(f"  ERROR: {name}: {err}")


if __name__ == "__main__":
    main()
