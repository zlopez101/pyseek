import configparser

from pyseek import SUCCESS, DIR_ERROR, FILE_ERROR, CONFIG_ERROR, __app_name__
from pathlib import Path
import typer

CONFIGURATION_DIRECTORY = typer.get_app_dir(__app_name__)


def create_file(
    configuration_directory: str = CONFIGURATION_DIRECTORY, filename: str = "config.ini"
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


def init_config(user_agent: str, config_file_dir: str = CONFIGURATION_DIRECTORY):
    """Called from the pyseek init command
    creates a configuration directory specified at config_file_dir
    and a configuration file in that directory called config.ini.
    The configuration file is a .ini file with a section called API
    """
    result = create_file(configuration_directory=config_file_dir)
    if result == SUCCESS:
        config = configparser.ConfigParser()
        config["API"] = {"User-Agent": user_agent}
        config["TickerUpdateFrequency"] = {"Frequency": "never"}
        try:
            with open(Path(config_file_dir) / "config.ini", "w") as configfile:
                config.write(configfile)
        except OSError:
            return CONFIG_ERROR
        return SUCCESS
    else:
        return result


def get_api_settings(config_path: Path) -> dict:
    config = configparser.ConfigParser()
    config.read(config_path)
    return list(config.items("API"))
