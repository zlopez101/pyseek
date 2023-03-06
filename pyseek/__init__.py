"""Top level package for pyseek."""

__app_name__ = "pyseek"
__version__ = "0.1.0"

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
