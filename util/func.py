import os

from util.constants import OUTPUT_DIRECTORY, TEMP_DIRECTORY, CONFIG_DIRECTORY, BIN_DIRECTORY, DIRECTORIES


def ensure_directories_exist():
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            os.mkdir(directory)


def get_output_file(filename: str):
    return os.path.join(OUTPUT_DIRECTORY, filename)


def get_temp_file(filename: str):
    return os.path.join(TEMP_DIRECTORY, filename)


def get_config_file(filename: str):
    return os.path.join(CONFIG_DIRECTORY, filename)


def get_bin_file(filename: str):
    return os.path.join(BIN_DIRECTORY, filename)