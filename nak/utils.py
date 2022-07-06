import os
import time
from pathlib import Path

from nak.conf import ZIP_EXCLUDE_FILES


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
        print(f'\r{current_time} INFO {prefix} | \033[5;32m{bar}\033[5;0m| {percent}% {suffix}', end=printEnd)

    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    # Print New Line on Complete
    print()


def get_all_file(path):
    list_file = os.listdir(path)
    all_files = []
    # Iterate over all the entries
    for entry in list_file:
        if any([exclude_file in entry for exclude_file in ZIP_EXCLUDE_FILES]):
            continue

        # Create full path
        fullPath = os.path.join(path, entry)

        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            all_files = all_files + get_all_file(fullPath)
        else:
            all_files.append(fullPath)
    return all_files
