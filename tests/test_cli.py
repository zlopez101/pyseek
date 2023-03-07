from typer.testing import CliRunner
from pyseek import __app_name__, __main__, __version__
from pyseek import setup

runner = CliRunner()


def test_version():
    result = runner.invoke(__main__.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_cli():
    result = runner.invoke(__main__.app, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output


def test_init_cli(configuration_directory):
    # test the help
    result = runner.invoke(__main__.app, ["init", "--help"])
    assert result.exit_code == 0
    assert "Initialize the user settings" in result.output

    # test the prompt
    result = runner.invoke(__main__.app, ["init", "--user-agent", "test_user_agent"])
    assert result.exit_code == 0

    # test the read_settings
    result = runner.invoke(__main__.app, ["settings"])
    assert result.exit_code == 0
    assert "test_user_agent" in result.output

    company_ticker_file = configuration_directory / "company_tickers.json"
    assert company_ticker_file.exists()
    text = company_ticker_file.read_text()
    for company in ["AAPL", "GOOG", "MSFT", "AMZN"]:
        assert company in text
