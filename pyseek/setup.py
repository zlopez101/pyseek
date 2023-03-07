from pathlib import Path

import typer

from pyseek import __app_name__

CONFIGURATION_DIRECTORY = typer.get_app_dir(__app_name__)
CONFIGURATION_FILE = Path(CONFIGURATION_DIRECTORY) / "config.ini"
