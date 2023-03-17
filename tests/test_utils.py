from pyseek import utils
import pytest
import requests


def test_utils_make_request(set_up, capsys):
    """Test the make_request function"""
    url = "https://httpbin.org/json"
    result = utils.make_request(url)
    assert isinstance(result, dict)

    # confirm header user-agent is set
    url = "https://httpbin.org/headers"
    result = utils.make_request(url)
    assert result["headers"]["User-Agent"] == "test_user_agent"

    # confirm timeout is set
    # and response is printed
    url = "https://httpbin.org/delay/8"
    utils.make_request(url, requestTimeout=3)
    captured = capsys.readouterr()
    assert "the server did not respond in time" in captured.out

    # confirm connection error is set
    url = "https://httpbin.org/status/404"
    with pytest.raises(requests.exceptions.HTTPError):
        utils.make_request(url)

    # confirm json decode error is caught
    # and response is printed
    url = "https://httpbin.org/"
    utils.make_request(url)
    captured = capsys.readouterr()
    assert "There was no JSON response for url: https://httpbin.org/" in captured.out


def test_set_headers(set_up):
    """Test the set_headers function"""
    result = utils.set_headers()
    assert result["User-Agent"] == "test_user_agent"
