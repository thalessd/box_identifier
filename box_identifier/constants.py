import os.path as path
from box_identifier.helpers import resource_path
from configparser import ConfigParser

config = ConfigParser()

config.read(resource_path("config.ini"))


def load_view(view_name):
    return resource_path("box_identifier/gui/{}".format(view_name))


DATA_FOLDER = resource_path("data")

LOAD_VIEW = load_view

PLACEHOLDER_BACKGROUND_LARGE = path.join(DATA_FOLDER, "background_large.png")

PLACEHOLDER_BACKGROUND_SMALL = path.join(DATA_FOLDER, "background_small.png")

DEFAULT_FONT = path.join(DATA_FOLDER, "bebas_neue.ttf")

APP_ICON = path.join(DATA_FOLDER, "icon.png")

GENERATED_DIR_NAME = "ADESIVOS PARA RAMAIS LOTE"

DROPBOX_ACCESS_TOKEN = config['APP']['DROPBOX_ACCESS_TOKEN']
