import logging
import os
import time

import yaml
from decouple import config as env_config

ENV_FILE_NAME = './.env'
ENV_FILE = os.path.abspath(ENV_FILE_NAME)

CONFIG_FILE_NAME = './config.yml'
CONFIG_FILE = os.path.abspath(CONFIG_FILE_NAME)

API_URL = 'https://accounts.29next.com'

ZIP_FILE_FORMAT = "{app_name}-" + time.strftime("%Y%m%d%H%M%S")
ZIP_DESTINATION = f'./tmp/{ZIP_FILE_FORMAT}.zip'
ZIP_EXCLUDE_FILES = ['.env', 'config.yml', 'tmp']


class Config(object):
    user_email = None
    password = None
    client_id = None

    env = 'development'

    user_email_required = False
    password_required = False
    client_id_required = False

    def __init__(self, **kwargs):
        self.read_config()
        for name, value in kwargs.items():
            setattr(self, name, value)

    def parser_config(self, parser, write_file=False):
        self.env = parser.env
        self.read_config()
        if getattr(parser, 'user_email', None):
            self.user_email = parser.user_email

        if getattr(parser, 'password', None):
            self.password = parser.password

        if getattr(parser, 'client_id', None):
            self.client_id = parser.client_id

        self.save(write_file)

    def read_config(self, update=True):
        configs = {}
        env = {}

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as yamlfile:
                configs = yaml.load(yamlfile, Loader=yaml.FullLoader)
                yamlfile.close()
            if configs and configs.get(self.env) and update:
                self.client_id = configs[self.env].get('client_id')

        if os.path.exists(ENV_FILE):
            env_config.search_path = os.getcwd()
            env['user_email'] = env_config('user_email', None)
            env['password'] = env_config('password', None)

            if update:
                self.user_email = env.get('user_email')
                self.password = env.get('password')

        return configs, env

    def validate_config(self):
        error_msgs = []
        if self.user_email_required and not self.user_email:
            error_msgs.append('-u/--user_email')
        if self.password_required and not self.password:
            error_msgs.append('-p/--password')
        if self.client_id_required and not self.client_id:
            error_msgs.append('-c/--client_id')

        if error_msgs:
            message = ', '.join(error_msgs)
            pluralize = 'is' if len(error_msgs) == 1 else 'are'
            raise TypeError(f'[{self.env}] argument {message} {pluralize} required.')

        return True

    def write_config(self):
        configs, env = self.read_config(update=False)

        new_config = {
            'client_id': self.client_id,
        }
        if configs.get(self.env) != new_config:
            configs[self.env] = new_config
            with open(CONFIG_FILE, 'w') as yamlfile:
                yaml.dump(configs, yamlfile)
                yamlfile.close()
            logging.info(f'[{self.env}] Configuration was updated.')

        if env.get('user_email') != self.user_email or env.get('password') != self.password:
            with open(ENV_FILE, 'w') as envfile:
                environments = "\n".join([
                    f'user_email={self.user_email}',
                    f'password={self.password}'
                ])
                envfile.writelines(environments)
            logging.info(f'[{self.env}] Environment was updated.')

    def save(self, write_file=True):
        if self.validate_config() and write_file:
            self.write_config()