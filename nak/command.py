import logging
import os
import time
import zipfile

from nak.conf import CONFIG_FILE, ENV_FILE, ZIP_DESTINATION, Config
from nak.decorator import parser_config
from nak.gateway import Gateway
from nak.utils import get_all_file, progress_bar

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Command(object):
    def __init__(self):
        self.config = Config()
        self.gateway = Gateway(
            email=self.config.user_email,
            password=self.config.password,
            client_id=self.config.client_id
        )

    @parser_config(
        user_email_required=True,
        password_required=True,
        client_id_required=True,
        write_file=True)
    def setup(self, parser):
        self.config.client_id = parser.client_id
        self.config.user_email = parser.user_email
        self.config.password = parser.password
        self.config.save()

        logging.info(f'[{self.config.env}] App with client_id[{parser.client_id}] has been setup successfully.')

    @parser_config()
    def build(self, parser):
        if not (os.path.exists(ENV_FILE) or os.path.exists(CONFIG_FILE)):
            raise TypeError(f'[{self.config.env}] Please check you is in correct directory.')

        app_name = os.getcwd().split('/')[-1]
        current_path = "."

        file_list = get_all_file(path=current_path)
        destination_file = ZIP_DESTINATION.format(app_name=app_name)

        # create directories
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

        new_zip = zipfile.ZipFile(destination_file, 'w')
        for file in progress_bar(file_list, prefix=f'[{self.config.env}] Progress:', suffix='Complete', length=50):
            time.sleep(0.05)
            new_zip.write(file)

        new_zip.close()
        logging.info(f'[{self.config.env}] Build successfully.')

    @parser_config()
    def push(self, parser):
        if not os.path.exists('tmp'):
            raise TypeError(f'[{self.config.env}] Please check you is in correct directory.')

        zip_directory = os.path.abspath("./tmp/")
        file_list = get_all_file(path=zip_directory)

        if not file_list:
            raise TypeError(f'[{self.config.env}] Please run build before push command.')

        latest_build_file = sorted(file_list, key=lambda file_name: file_name, reverse=True)[0]
        file_name = latest_build_file.split("/")[-1]

        logging.info(f'[{self.config.env}] Pushing to app with client_id {self.config.client_id}')
        logging.info(f'[{self.config.env}] with filename {file_name}')
        logging.info(f'[{self.config.env}] by username {self.config.user_email}')

        files = {'file': (latest_build_file, open(latest_build_file, 'rb'))}
        response = self.gateway.update_app(files=files)
        if not response.ok:
            return

        logging.info(f'[{self.config.env}] Push update file to app successfully.')
