"""Sets the configuration files for pyseek, handles reading and writing to the configuration files"""

import configparser
from typing import List
from pyseek import SUCCESS, DIR_ERROR, FILE_ERROR, CONFIG_ERROR
from pathlib import Path
from pyseek import setup


def create_file(
    configuration_directory: str = setup.CONFIGURATION_DIRECTORY,
    filename: str = "config.ini",
) -> int:
    """Take a configuration directory and create a file in it.

    Args:
        configuration_directory (str): the configuration directory
        filename (str, optional): the name of the file to create. Defaults to "config.ini".

    Returns:
        int: the result code of the operation
    """
    try:
        configuration_directory = Path(configuration_directory)
        configuration_directory.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        configuration_file = configuration_directory / filename
        configuration_file.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS


def init_config(user_agent: str):
    """Called from the pyseek init command
    creates a configuration directory specified at config_file_dir
    and a configuration file in that directory called config.ini.
    The configuration file is a .ini file with a section called API
    """
    f = "config.ini"
    result = create_file(filename=f)
    if result == SUCCESS:
        config = configparser.ConfigParser()
        config["API"] = {"User-Agent": user_agent}
        config["TickerUpdateFrequency"] = {"Frequency": "never"}
        try:
            with open(Path(setup.CONFIGURATION_DIRECTORY) / f, "w") as configfile:
                config.write(configfile)
        except OSError:
            return CONFIG_ERROR
        return SUCCESS
    else:
        return result


def get_api_settings() -> configparser.SectionProxy:
    """Get the API settings from the config file"""
    settings_file = Path(setup.CONFIGURATION_DIRECTORY) / "config.ini"
    config = configparser.ConfigParser()
    config.read(settings_file)
    return config["API"]


if __name__ == "__main__":
    setting = get_api_settings()
    print(setting)
