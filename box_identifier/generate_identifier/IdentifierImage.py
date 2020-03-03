from PIL import Image, ImageDraw, ImageFont


class IdentifierImage:

    is_pac = False
    is_small = True

    __identifier_str = ''
    __image_path = ''
    __font_path = ''

    def __init__(self, identifier_str, image_path, font_path):
        self.__identifier_str = identifier_str
        self.__image_path = image_path
        self.__font_path = font_path

    def save(self, out_path):
        image = self.__generate_image()

        image.save(out_path)

    def show(self):
        image = self.__generate_image()

        image.show()

    def image(self):
        return self.__generate_image()

    def __generate_image(self):
        bg = Image.open(self.__image_path).convert("RGBA")

        txt = Image.new('RGBA', bg.size, (255, 255, 255, 0))

        bg_width, bg_height = bg.size

        bg_scale = bg_width + bg_height / 2

        font_size = self.__config_font_size(bg_scale)

        font = ImageFont.truetype(self.__font_path, font_size)

        d_ctx = ImageDraw.Draw(txt)

        text_width, text_height = d_ctx.textsize(self.__identifier_str, font)

        text_x_position = (bg_width - text_width) / 2

        text_y_position = self.__config_y_position(bg_scale)

        d_ctx.text(
            (text_x_position, text_y_position),
            self.__identifier_str,
            font=font,
            fill=(255, 255, 255, 255)
        )

        return Image.alpha_composite(bg, txt)

    def __config_font_size(self, bg_scale):
        if self.is_small:
            return int(bg_scale * (0.093 if self.is_pac else 0.12))
        else:
            return int(bg_scale * (0.086 if self.is_pac else 0.13))

    def __config_y_position(self, bg_scale):
        if self.is_small:
            return int(bg_scale * (0.585 if self.is_pac else 0.57))
        else:
            return int(bg_scale * (0.80 if self.is_pac else 0.772))