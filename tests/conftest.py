import pytest
from pyseek import setup


@pytest.fixture
def test_dir(tmp_path):
    """Create a test directory"""
    temporary_directory = tmp_path / "pyseek"
    temporary_directory.mkdir()
    return temporary_directory


@pytest.fixture
def configuration_directory(monkeypatch, tmp_path):
    """mock the configuration directory for testing"""
    monkeypatch.setattr(setup, "CONFIGURATION_DIRECTORY", tmp_path.as_posix())
    return tmp_path


# @pytest.fixture
# def set_up(configuration_directory):
#     """Set up the test environment"""
#     config.init_config("test_user_agent")
#     return configuration_directory
