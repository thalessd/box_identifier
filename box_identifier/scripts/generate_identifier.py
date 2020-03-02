import os.path
import shutil
from datetime import datetime
from .make_image import make_image
from .make_identifier_list import make_identifier_list
from .helpers import random_hex_uppercase


def _resolve_progress(current_idx, tot_items):
    return int(current_idx * 100 / tot_items)


def _progress(percent):
    return


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

    dir_name = "ADESIVOS PARA RAMAIS LOTE {}_{}".format(
        lot,
        now.strftime("%d_%m_%Y_%H_%M_%S"),
    )

    dir_path = os.path.join(out_path, dir_name)

    os.mkdir(dir_path)

    identifier_list = make_identifier_list(
        r_init, r_end,
        ct_init, ct_end,
        pac_init, pac_end
    )

    file_paths = []

    for idx, identifier in enumerate(identifier_list, 1):

        file_name = "{}-{}.png".format(
            identifier,
            lot
        )

        file_path = os.path.join(dir_path, file_name)

        if make_zip:
            file_paths.append(file_path)

        is_pac = pac_init is not None and pac_end is not None

        make_image(background_path, font_path, identifier, file_path, is_pac, is_small)

        percent = _resolve_progress(idx, len(identifier_list))

        progress(percent)

    if make_zip:
        shutil.make_archive(dir_path, "zip", dir_path)
        shutil.rmtree(dir_path)
