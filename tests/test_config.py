from pyseek import config
from pyseek import SUCCESS, DIR_ERROR, FILE_ERROR, CONFIG_ERROR


def test__init_config_file(configuration_directory):
    """Test the _init_config_file function"""
    test_dir = configuration_directory / "test_dir"
    test_dir.mkdir(exist_ok=True)
    result = config.create_file(configuration_directory=test_dir)
    assert result == SUCCESS
    config_file = test_dir / "config.ini"
    assert config_file.exists()


def test_init_config_and_read_settings(configuration_directory):
    """Test the init_config function"""
    result = config.init_config("test_user_agent")
    assert result == SUCCESS
    config_file = configuration_directory / "config.ini"
    assert config_file.exists()
    assert config_file.is_file()
    content = config_file.read_text()
    assert "test_user_agent" in content


# def test_get_api_settings(set_up):
#     assert not setup.CONFIGURATION_DIRECTORY == "/home/zlopez/.config/pyseek"
#     settings = config.get_api_settings()
#     assert settings
#     assert "test_user_agent" in settings[0]
