import logging
import os

import yaml
from decouple import config as env_config

from nak.settings import CONFIG_FILE, ENV_FILE, LOG_COLOR


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
        new_configs = {
            'client_id': self.client_id
        }
        if not configs or configs != new_configs:
            with open(CONFIG_FILE, 'w') as yamlfile:
                yaml.dump({
                    'client_id': self.client_id
                }, yamlfile)
                yamlfile.close()

            logging.info(LOG_COLOR.INFO.format(message='Configuration was updated.'))

        new_env = {
            'email': self.email,
            'password': self.password
        }
        if not env or env != new_env:
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
