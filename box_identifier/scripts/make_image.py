from PIL import Image, ImageDraw, ImageFont
from box_identifier.scripts.helpers import resource_path


def make_image(image_path, identifier_str, out_path, is_pac=False):

    image_path_normalized = resource_path(image_path)

    font_path_normalized = resource_path("../../data/bebas_neue.ttf")

    bg = Image.open(image_path_normalized).convert("RGBA")

    txt = Image.new('RGBA', bg.size, (255, 255, 255, 0))

    bg_width, bg_height = bg.size

    bg_scale = bg_width * bg_height / 2

    font_size = int(bg_scale * (0.00023 if is_pac else 0.00034))

    text_y_position = int(bg_scale * (0.00223 if is_pac else 0.00216))

    font = ImageFont.truetype(font_path_normalized, font_size)

    d_ctx = ImageDraw.Draw(txt)

    text_width, text_height = d_ctx.textsize(identifier_str, font)

    text_x_position = (bg_width - text_width) / 2

    d_ctx.text(
        (text_x_position, text_y_position),
        identifier_str,
        font=font,
        fill=(255, 255, 255, 255)
    )

    image = Image.alpha_composite(bg, txt)

    image.save(out_path)
