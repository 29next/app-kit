import logging
import os
import zipfile

from nak.config import Config
from nak.gateway import Gateway
from nak.settings import (CONFIG_FILE, ENV_FILE, LOG_COLOR,
                          ZIP_DESTINATION_DIRECTORY, ZIP_DESTINATION_PATH)
from nak.utils import (get_all_file, get_error_from_response, hide_variable,
                       progress_bar)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Command(object):
    def __init__(self):
        self.config = Config()
        self.gateway = Gateway(
            email=self.config.email,
            password=self.config.password,
            client_id=self.config.client_id
        )

    def setup(self, parser=None):
        self.config.client_id = input(
            f"App Client ID [{hide_variable(self.config.client_id)}]: ") or self.config.client_id
        self.config.email = input(
            f"accounts.29next.com Email [{self.config.email}]: ") or self.config.email
        self.config.password = input(
            f"accounts.29next.com Password [{hide_variable(self.config.password, True)}]: ") or self.config.password
        self.config.save()

        logging.info(LOG_COLOR.SUCCESS.format(
            message=f'App with client_id {self.config.client_id} has been setup successfully.'
        ))

    def build(self, parser=None):
        if not (os.path.exists(ENV_FILE) or os.path.exists(CONFIG_FILE)):
            raise TypeError(LOG_COLOR.ERROR.format(
                message=(
                    'Unable to locate config or env file. '
                    'You can configure config or env file by running "nak setup".')))

        app_name = os.getcwd().split('/')[-1]
        current_path = "."

        file_list = get_all_file(path=current_path)
        for file in file_list:
            logging.info(LOG_COLOR.INFO.format(message=f'file: {file}'))

        destination_file = ZIP_DESTINATION_PATH.format(app_name=app_name)

        # create directories
        if not os.path.exists(ZIP_DESTINATION_DIRECTORY):
            os.mkdir(ZIP_DESTINATION_DIRECTORY)

        new_zip = zipfile.ZipFile(destination_file, 'w')
        for file in progress_bar(file_list, prefix='Progress:', suffix='Complete', length=50):
            new_zip.write(file)

        new_zip.close()
        logging.info(LOG_COLOR.SUCCESS.format(message='Build successfully.'))

    def push(self, parser=None):
        if not (os.path.exists(ENV_FILE) or os.path.exists(CONFIG_FILE)):
            raise TypeError(LOG_COLOR.ERROR.format(
                message=(
                    'Unable to locate config or env file. '
                    'You can configure config or env file by running "nak setup".')))

        if not os.path.exists(ZIP_DESTINATION_DIRECTORY):
            raise TypeError(LOG_COLOR.ERROR.format(
                message=('No build file available. Run "nak build".')))

        zip_file_list = get_all_file(path=f"./{ZIP_DESTINATION_DIRECTORY}", required_extension='.zip')
        if not zip_file_list:
            raise TypeError(LOG_COLOR.ERROR.format(message='Please run build before push command.'))

        latest_build_file = sorted(zip_file_list, key=lambda file_name: file_name, reverse=True)[0]
        file_name = latest_build_file.split("/")[-1]

        logging.info(LOG_COLOR.INFO.format(message=f'Pushing to app with client_id {self.config.client_id}'))
        logging.info(LOG_COLOR.INFO.format(message=f'with filename {file_name}'))
        logging.info(LOG_COLOR.INFO.format(message=f'by username {self.config.email}'))

        files = {'file': (latest_build_file, open(f'{latest_build_file}', 'rb'))}

        response = self.gateway.update_app(files=files)
        if not response.ok:
            error_msg = get_error_from_response(response)
            logging.info(LOG_COLOR.ERROR.format(message=f'Upload file to server failed. {error_msg}'))
            return

        logging.info(LOG_COLOR.SUCCESS.format(message='Push update file to app successfully.'))
