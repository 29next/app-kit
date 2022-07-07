import logging
import os
import time

import yaml
from decouple import config as env_config

ENV_FILE_NAME = './.env'
ENV_FILE = os.path.abspath(ENV_FILE_NAME)

CONFIG_FILE_NAME = './config.yml'
CONFIG_FILE = os.path.abspath(CONFIG_FILE_NAME)


# API_URL = 'https://accounts.29next.com'
API_URL = 'http://localhost:1111'

ZIP_FILE_FORMAT = "{app_name}-" + time.strftime("%Y%m%d%H%M%S")
ZIP_DESTINATION_DIRECTORY = '.tmp'
ZIP_DESTINATION_PATH = f'./{ZIP_DESTINATION_DIRECTORY}/{ZIP_FILE_FORMAT}.zip'
ZIP_EXCLUDE_FILES = ['.env', 'config.yml', ZIP_DESTINATION_DIRECTORY]

CONTENT_FILE_EXTENSIONS = ['.html', '.json', '.css', '.scss', '.js']
MEDIA_FILE_EXTENSIONS = [
    '.woff2', '.gif', '.ico', '.png', '.jpg', '.jpeg', '.svg', '.eot', '.tff', '.ttf', '.woff',
    '.webp', '.mp4', '.webm', '.mp3', '.pdf',
]
ALLOW_FILE_EXTENSIONS = CONTENT_FILE_EXTENSIONS + MEDIA_FILE_EXTENSIONS


class LOG_COLOR:
    ERROR = '\x1b[31;10m{message}\x1b[0m'
    SUCCESS = '\x1b[32;10m{message}\x1b[0m'
    INFO = '\x1b[36;10m{message}\x1b[0m'


class Config(object):
    email = None
    password = None
    client_id = None

    def __init__(self):
        configs, env = self.read_config()

        self.client_id = configs.get('client_id')
        self.email = env.get('email')
        self.password = env.get('password')

    def read_config(self):
        configs = {}
        env = {}

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as yamlfile:
                configs = yaml.load(yamlfile, Loader=yaml.FullLoader) or {}
                yamlfile.close()

        if os.path.exists(ENV_FILE):
            env_config.search_path = os.getcwd()
            env['email'] = env_config('email', None)
            env['password'] = env_config('password', None)

        return configs, env

    def validate_config(self):
        error_msgs = []
        if not self.client_id:
            error_msgs.append('client_id')
        if not self.email:
            error_msgs.append('email')
        if not self.password:
            error_msgs.append('password')

        if error_msgs:
            message = ', '.join(error_msgs)
            pluralize = 'is' if len(error_msgs) == 1 else 'are'
            raise TypeError(LOG_COLOR.ERROR.format(
                message=f'argument {message} {pluralize} required.'
            ))

        return True

    def write_config(self):
        configs, env = self.read_config()
        if not configs or configs.get('client_id') != self.client_id:
            with open(CONFIG_FILE, 'w') as yamlfile:
                yaml.dump({
                    'client_id': self.client_id
                }, yamlfile)
                yamlfile.close()

            logging.info(LOG_COLOR.INFO.format(message='Configuration was updated.'))

        if not env or env.get('email') != self.email or env.get('password') != self.password:
            with open(ENV_FILE, 'w') as envfile:
                environments = "\n".join([
                    f'email={self.email}',
                    f'password={self.password}'
                ])
                envfile.writelines(environments)
            logging.info(LOG_COLOR.INFO.format(message='Environment was updated.'))

    def save(self):
        if not self.validate_config():
            return
        self.write_config()
