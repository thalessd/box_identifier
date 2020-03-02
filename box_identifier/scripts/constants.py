import os.path as path
from .helpers import resource_path

DATA_FOLDER = resource_path("data")

VIEWS_FOLDER = resource_path("views")

PLACEHOLDER_BACKGROUND_LARGE = path.join(DATA_FOLDER, "background_large.png")

PLACEHOLDER_BACKGROUND_SMALL = path.join(DATA_FOLDER, "background_small.png")

DEFAULT_FONT = path.join(DATA_FOLDER, "bebas_neue.ttf")

APP_ICON = path.join(DATA_FOLDER, "icon.png")

GENERATED_DIR_NAME = "ADESIVOS PARA RAMAIS LOTE"
