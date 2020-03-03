from box_identifier import app_run, IdentifierImage, generate_identifier, constants


def placeholder_progres(percent):
    print(percent)


if __name__ == '__main__':
    print("")
    # image_identifier = IdentifierImage("Str_test", constants.PLACEHOLDER_BACKGROUND_SMALL, constants.DEFAULT_FONT)
    #
    # image_identifier.is_pac = True
    #
    # image_identifier.save("./teste.png")

    # app_run()

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
        progress=placeholder_progres,
    )

