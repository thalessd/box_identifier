import dropbox
import tempfile
from urllib import request
from os import path
from box_identifier import constants


class DropBox:

    __dropbox = None

    def __init__(self):

        access_token = constants.DROPBOX_ACCESS_TOKEN

        self.__dropbox = dropbox.Dropbox(access_token)

    def all_file_names(self):

        file_dicts = []

        files_list = self.__dropbox.files_list_folder(path="").entries

        for file in files_list:

            filename = file.name.split(".")[0]

            file_dict = dict(filename=filename, path=file.path_lower)

            file_dicts.append(file_dict)

        return file_dicts

    def get_temp_file_path(self, dropbox_path):
        temporary_link = self.__dropbox.files_get_temporary_link(dropbox_path)
        url = temporary_link.link

        response = request.urlopen(url)
        data = response.read()

        temp_dir = tempfile.gettempdir()

        file_name = path.join(temp_dir, "box_identifier")

        open(file_name, 'wb').write(data)

        return file_name


