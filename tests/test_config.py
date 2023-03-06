from pyseek.config import (
    get_api_settings,
    init_config,
    # create_configuration_file,
    create_file,
)
from pyseek import SUCCESS, DIR_ERROR, FILE_ERROR, CONFIG_ERROR


def test__init_config_file(tmp_path):
    """Test the _init_config_file function"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(exist_ok=True)
    result = create_file(test_dir)
    assert result == SUCCESS
    config = test_dir / "config.ini"
    assert config.exists()


def test_init_config_and_read_settings(tmp_path):
    """Test the init_config function"""
    result = init_config("test_user_agent", tmp_path)
    assert result == SUCCESS
    config_file = tmp_path / "config.ini"
    assert config_file.exists()
    assert config_file.is_file()
    content = config_file.read_text()
    assert "test_user_agent" in content


def test_temp_dir(tmp_path):
    """Test the temp_dir fixture"""
    assert tmp_path.exists()
    configuration_path = tmp_path / "config.ini"
    assert not configuration_path.exists()
    configuration_path.touch(exist_ok=True)
    assert configuration_path.exists()
