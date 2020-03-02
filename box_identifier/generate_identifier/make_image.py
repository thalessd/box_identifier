from PIL import Image, ImageDraw, ImageFont


def config_font_size(bg_scale, is_pac, is_small):
    if is_small:
        return int(bg_scale * (0.093 if is_pac else 0.12))
    else:
        return int(bg_scale * (0.086 if is_pac else 0.13))


def config_y_position(bg_scale, is_pac, is_small):
    if is_small:
        return int(bg_scale * (0.585 if is_pac else 0.57))
    else:
        return int(bg_scale * (0.80 if is_pac else 0.772))


def make_image(image_path, font_path, identifier_str, out_path, is_pac=False, is_small=True):

    bg = Image.open(image_path).convert("RGBA")
    txt = Image.new('RGBA', bg.size, (255, 255, 255, 0))

    bg_width, bg_height = bg.size

    bg_scale = bg_width + bg_height / 2

    font_size = config_font_size(bg_scale, is_pac, is_small)

    font = ImageFont.truetype(font_path, font_size)

    d_ctx = ImageDraw.Draw(txt)

    text_width, text_height = d_ctx.textsize(identifier_str, font)

    text_x_position = (bg_width - text_width) / 2

    text_y_position = config_y_position(bg_scale, is_pac, is_small)

    d_ctx.text(
        (text_x_position, text_y_position),
        identifier_str,
        font=font,
        fill=(255, 255, 255, 255)
    )

    image = Image.alpha_composite(bg, txt)

    image.save(out_path)
