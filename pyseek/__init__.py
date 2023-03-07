"""Top level package for pyseek."""

__app_name__ = "pyseek"
__version__ = "0.2.0"
# from typer import get_app_dir

# CONFIGURATION_DIRECTORY = get_app_dir(__app_name__)


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    CONFIG_ERROR,
) = range(4)

ERRORS = {
    DIR_ERROR: "Configurations directory could not be created.",
    FILE_ERROR: "Configurations file could not be created.",
    CONFIG_ERROR: "Configurations file could not be written.",
}
