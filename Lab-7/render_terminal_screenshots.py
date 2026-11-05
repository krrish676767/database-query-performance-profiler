import os
import re
from PIL import Image, ImageDraw, ImageFont

def render_terminal_window(
    title,
    lines,
    output_path,
    width=1100,
    font_size=15,
    line_spacing=4,
    padding=24
):
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', font_size)
        bold_font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', font_size)
    except Exception:
        font = ImageFont.load_default()
        bold_font = font

    # Calculate content height
    header_height = 42
    line_height = font_size + line_spacing
    content_height = len(lines) * line_height + padding * 2
    height = header_height + content_height

    # Create base image with soft outer margin for drop shadow
    margin = 20
    img_w = width + margin * 2
    img_h = height + margin * 2

    # Canvas (transparent or dark outer background)
    canvas = Image.new("RGBA", (img_w, img_h), (245, 247, 250, 255))
    draw = ImageDraw.Draw(canvas)

    # Shadow
    for i in range(margin):
        alpha = int(35 * (1 - (i / margin)))
        shadow_rect = [
            margin - i,
            margin - i,
            img_w - margin + i,
            img_h - margin + i
        ]
        draw.rounded_rectangle(shadow_rect, radius=14, fill=(0, 0, 0, alpha))

    # Window body rect
    win_rect = [margin, margin, margin + width, margin + height]
    draw.rounded_rectangle(win_rect, radius=10, fill=(30, 30, 30, 255))

    # Window title bar
    title_rect = [margin, margin, margin + width, margin + header_height]
    draw.rounded_rectangle(title_rect, radius=10, fill=(45, 45, 45, 255))
    draw.rectangle([margin, margin + header_height - 10, margin + width, margin + header_height], fill=(45, 45, 45, 255))

    # Traffic lights (macOS buttons)
    btn_y = margin + header_height // 2
    btn_r = 6
    draw.ellipse([margin + 18 - btn_r, btn_y - btn_r, margin + 18 + btn_r, btn_y + btn_r], fill=(255, 95, 86, 255))
    draw.ellipse([margin + 38 - btn_r, btn_y - btn_r, margin + 38 + btn_r, btn_y + btn_r], fill=(255, 189, 46, 255))
    draw.ellipse([margin + 58 - btn_r, btn_y - btn_r, margin + 58 + btn_r, btn_y + btn_r], fill=(39, 201, 63, 255))

    # Window title text
    title_font = font
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text((margin + (width - title_w) // 2, margin + (header_height - (bbox[3] - bbox[1])) // 2 - 2), title, font=title_font, fill=(180, 180, 180, 255))

    # Render terminal lines with syntax coloring
    curr_y = margin + header_height + padding
    for line in lines:
        curr_x = margin + padding
        for chunk in line:
            text = chunk.get("text", "")
            color = chunk.get("color", (220, 220, 220, 255))
            is_bold = chunk.get("bold", False)
            f = bold_font if is_bold else font
            draw.text((curr_x, curr_y), text, font=f, fill=color)
            cb = draw.textbbox((0, 0), text, font=f)
            curr_x += (cb[2] - cb[0])
        curr_y += line_height

    canvas.save(output_path, "PNG")
    print(f"Saved: {output_path}")

print("Screenshot generator module ready.")
