from box_identifier import app_run, generate_identifier, constants


def placeholder_progres(percent):
    print(percent)


if __name__ == '__main__':

    app_run()

    # generate_identifier(
    #     background_path=constants.PLACEHOLDER_BACKGROUND_SMALL,
    #     font_path=constants.DEFAULT_FONT,
    #     out_path="./",
    #     make_zip=True,
    #     r_init=1,
    #     r_end=4,
    #     ct_init=1,
    #     ct_end=4,
    #     is_small=True,
    #     progress=placeholder_progres,
    # )
