import dropbox
from box_identifier import constants


class DropBox:

    def __init__(self):

        pass
        # o_auth2 = dropbox.DropboxOAuth2FlowNoRedirect(
        #     constants.DROPBOX_APP_KEY,
        #     constants.DROPBOX_SECRET_KEY,
        # )
        #
        # access_token = o_auth2.finish()
        #
        # print(access_token)
        #
        # dbx = dropbox.Dropbox(access_token)
        #
        # result = dbx.files_list_folder(path="")
        #
        # print(result)
