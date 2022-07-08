import os
import time
from pathlib import Path

from nak.settings import ALLOW_FILE_EXTENSIONS, ZIP_EXCLUDE_FILES


def get_latest_zip(pathfile):
    return Path(os.path.relpath(pathfile)).as_posix()


def progress_bar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    if total == 0:
        return

    # Progress Bar Printing Function
    def print_progress_bar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\r{current_time} INFO {prefix} | \033[1;32m{bar}\033[1;0m| {percent}% {suffix}', end=printEnd)

    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    # Print New Line on Complete
    print()


def get_all_file(path, required_extension=None):
    list_file = os.listdir(path)
    all_files = []
    for entry in list_file:
        extension = os.path.splitext(entry)[1]
        if any([exclude_file in entry for exclude_file in ZIP_EXCLUDE_FILES]) or \
                (extension != required_extension and not (os.path.isdir(entry) or extension in ALLOW_FILE_EXTENSIONS)):
            continue

        fullPath = os.path.join(path, entry)
        if os.path.isdir(fullPath):
            all_files = all_files + get_all_file(fullPath)
        else:
            all_files.append(fullPath)
    return all_files


def hide_variable(value, all=False):
    if not value:
        return
    return "********" if all else f"********{value[-8:]}"


def get_error_from_response(response):
    result = response.json()
    error_msg = ""
    for key, value in result.items():
        if type(value) == list:
            error_msg += f'"{key}" : {" ".join(value)}'
        else:
            error_msg += value

    return error_msg
