import os.path
import shutil
from datetime import datetime
from box_identifier.helpers import random_hex_uppercase
from box_identifier.constants import GENERATED_DIR_NAME
from .IdentifierImage import IdentifierImage
from .Identifiers import Identifiers


def _resolve_progress(current_idx, tot_items):
    return int(current_idx * 100 / tot_items)


def _progress(percent):
    return percent


def generate_identifier(
        background_path,
        font_path,
        out_path,
        make_zip,
        r_init, r_end,
        ct_init, ct_end,
        pac_init=None, pac_end=None,
        is_small=True,
        progress=_progress,
):

    now = datetime.now()

    lot = random_hex_uppercase(6)

    dir_name = "{} {}_{}".format(
        GENERATED_DIR_NAME,
        lot,
        now.strftime("%d_%m_%Y_%H_%M_%S"),
    )

    dir_path = os.path.join(out_path, dir_name)

    os.mkdir(dir_path)

    identifiers = Identifiers(
        r_init, r_end,
        ct_init, ct_end,
        pac_init, pac_end
    )

    identifiers_list = identifiers.list()

    file_paths = []

    for idx, identifier in enumerate(identifiers_list, 1):

        file_name = "{}-{}.png".format(
            identifier,
            lot
        )

        file_path = os.path.join(dir_path, file_name)

        if make_zip:
            file_paths.append(file_path)

        is_pac = pac_init is not None and pac_end is not None

        identifier_image = IdentifierImage(identifier, background_path, font_path)

        identifier_image.is_pac = is_pac

        identifier_image.is_small = is_small

        identifier_image.save(file_path)

        percent = _resolve_progress(idx, len(identifiers_list))

        progress(percent)

    if make_zip:
        shutil.make_archive(dir_path, "zip", dir_path)
        shutil.rmtree(dir_path)
