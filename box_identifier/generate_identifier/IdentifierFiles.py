import os.path
import shutil
from datetime import datetime
from box_identifier.helpers import random_hex_uppercase
from box_identifier.constants import GENERATED_DIR_NAME
from .IdentifierImage import IdentifierImage
from .Identifiers import Identifiers


class IdentifierFiles:

    make_zip = False
    is_small = True

    __identifiers_list = []

    def __init__(self, background_path, font_path,
                 r_init, r_end, ct_init, ct_end, pac_init=None, pac_end=None):

        self.background_path = background_path
        self.font_path = font_path

        self.r_init = r_init
        self.r_end = r_end
        self.ct_init = ct_init
        self.ct_end = ct_end
        self.pac_init = pac_init
        self.pac_end = pac_end

        identifiers = Identifiers(
            self.r_init, self.r_end,
            self.ct_init, self.ct_end,
            self.pac_init, self.pac_end
        )

        self.__identifiers_list = identifiers.list()

    def save(self, out_path, progress=None):
        self.__files_generate(out_path, progress)

    def file_list_size(self):
        return len(self.__identifiers_list)

    @staticmethod
    def __resolve_progress(current_idx, tot_items):
        return int(current_idx * 100 / tot_items)

    @staticmethod
    def __resolve_dir_path(out_path, lot):
        now = datetime.now()

        dir_name = "{} {}_{}".format(
            GENERATED_DIR_NAME,
            lot,
            now.strftime("%d_%m_%Y_%H_%M_%S"),
        )

        return os.path.join(out_path, dir_name)

    def __files_generate(self, out_path, progress=None):

        lot = random_hex_uppercase(6)

        dir_path = self.__resolve_dir_path(out_path, lot)

        os.mkdir(dir_path)

        file_paths = []

        for idx, identifier in enumerate(self.__identifiers_list, 1):

            file_name = "{}-{}.png".format(
                identifier,
                lot
            )

            file_path = os.path.join(dir_path, file_name)

            if self.make_zip:
                file_paths.append(file_path)

            is_pac = self.pac_init is not None and self.pac_end is not None

            identifier_image = IdentifierImage(identifier, self.background_path, self.font_path)

            identifier_image.is_pac = is_pac

            identifier_image.is_small = self.is_small

            identifier_image.save(file_path)

            if progress:
                percent = self.__resolve_progress(idx, len(self.__identifiers_list))

                progress(int(percent))

        if self.make_zip:
            shutil.make_archive(dir_path, "zip", dir_path)
            shutil.rmtree(dir_path)
