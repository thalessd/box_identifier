import box_identifier.scripts.constants as constants
from box_identifier.scripts.generate_identifier import generate_identifier


def progress(percent):
    print(percent)


if __name__ == '__main__':
    generate_identifier(
        background_path=constants.PLACEHOLDER_BACKGROUND_SMALL,
        font_path=constants.DEFAULT_FONT,
        out_path="./",
        make_zip=True,
        r_init=1,
        r_end=4,
        ct_init=1,
        ct_end=4,
        is_small=True,
        progress=progress,
    )
