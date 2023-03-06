import pytest
from pyseek import config


@pytest.fixture
def test_dir(tmp_path):
    """Create a test directory"""
    temporary_directory = tmp_path / "pyseek"
    temporary_directory.mkdir()
    return temporary_directory


@pytest.fixture()
def configuration_directory(monkeypatch, tmp_path):
    """mock the configuration directory for testing"""
    monkeypatch.setattr(config, "CONFIGURATION_DIRECTORY", tmp_path.as_posix())
    return tmp_path


# @pytest.fixture(scope="session")
# def config_file_dir(tmp_path):
#     """Create a configuration file directory"""
#     from pyseek.config import init_config
