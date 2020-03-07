from box_identifier import app_run, IdentifierImage, IdentifierFiles, constants
from box_identifier.services import DropBox


def placeholder_progress(percent):
    print(percent)


if __name__ == '__main__':
    # image_identifier = IdentifierImage("Str_test", constants.PLACEHOLDER_BACKGROUND_SMALL, constants.DEFAULT_FONT)
    #
    # image_identifier.is_pac = True
    #
    # image_identifier.save("./teste.png")

    app_run()
    #
    # identifier_files = IdentifierFiles(
    #     background_path=constants.PLACEHOLDER_BACKGROUND_SMALL,
    #     font_path=constants.DEFAULT_FONT,
    #     out_path="./",
    #     r_init=1,
    #     r_end=4,
    #     ct_init=1,
    #     ct_end=4,
    # )
    #
    # identifier_files.make_zip = False
    #
    # identifier_files.is_small = True
    #
    # identifier_files.save("./", placeholder_progress)

    # drop_box = DropBox()
    #
    # file_list = drop_box.all_file_names()
    #
    # drop_box.get_temp_file_path(file_list[1]["path"])

    pass

