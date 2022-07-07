import os
import time

ENV_FILE_NAME = './.env'
ENV_FILE = os.path.abspath(ENV_FILE_NAME)

CONFIG_FILE_NAME = './config.yml'
CONFIG_FILE = os.path.abspath(CONFIG_FILE_NAME)

API_URL = 'https://accounts.29next.com'

ZIP_FILE_FORMAT = "{app_name}-" + time.strftime("%Y%m%d%H%M%S")
ZIP_DESTINATION_DIRECTORY = '.tmp'
ZIP_DESTINATION_PATH = f'./{ZIP_DESTINATION_DIRECTORY}/{ZIP_FILE_FORMAT}.zip'
ZIP_EXCLUDE_FILES = ['.env', 'config.yml', ZIP_DESTINATION_DIRECTORY]

ALLOW_FILE_EXTENSIONS = [
    # CONTENT_FILE_EXTENSIONS
    '.html', '.json', '.css', '.scss', '.js',

    # MEDIA_FILE_EXTENSIONS
    '.woff2', '.gif', '.ico', '.png', '.jpg', '.jpeg', '.svg', '.eot', '.tff', '.ttf', '.woff',
    '.webp', '.mp4', '.webm', '.mp3', '.pdf'
]


class LOG_COLOR:
    ERROR = '\x1b[31;10m{message}\x1b[0m'
    SUCCESS = '\x1b[32;10m{message}\x1b[0m'
    INFO = '\x1b[36;10m{message}\x1b[0m'
