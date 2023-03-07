import json
import os
from typing import TypeVar

import requests
from pathlib import Path
from pyseek import models
from pyseek import setup
from pyseek import config


SAMPLE_HEADERS = {
    "User-Agent": "Zach Lopez (zachlopez9@gmail.com)",
}

centralIndexKey = TypeVar("centralIndexKey", str, int, models.CIK)


def make_request(url: str) -> dict:
    """Handles all the requests calls for the package

    Args:
        url (str): url to request

    Returns:
        dict: the json returned
    """
    try:
        config.get_api_settings()
        r = requests.get(url, headers=SAMPLE_HEADERS)
        r.raise_for_status()
        return r.json()
    except requests.JSONDecodeError:
        print("there was nothing to return")
    except requests.ConnectionError:
        print("there was a connection error")


def company_from_ticker(ticker: str) -> int:
    """Use the company_tickers.json file downloaded in `pyseek init` to get the CIK number for the company

    Args:
        ticker (str): ticker to look up

    Returns:
        int: company information for a given ticker
    """
    ticker = ticker.upper()
    with open(Path(setup.CONFIGURATION_DIRECTORY) / "company_tickers.json", "r") as fp:
        data = json.load(fp)
    return [company for company in data.values() if company["ticker"] == ticker]


def company_from_cik(cik: int) -> str:
    """Use the company_tickers.json file downloaded in `pyseek init` to get the ticker for the company

    Args:
        cik (int): cik number to look up

    Returns:
        str: company information for given cik number
    """
    with open(Path(setup.CONFIGURATION_DIRECTORY) / "company_tickers.json", "r") as fp:
        data = json.load(fp)
    return [company for company in data.values() if company["cik_str"] == cik]


def validate_cik(cik) -> int:
    """Validate the CIK for function

    Args:
        cik (One of CIK, str, int): The central index key to look up

    Returns:
        int: the properly formatted string
    """
    if isinstance(cik, models.CIK):
        return cik.cik_str
    else:
        # check if the cik can be interpreted as a number, if not then continue
        assert int(cik), "Please use a string that can be interpreted as a number"

        # get the cik all the way to 10 digits long
        temp = str(cik)
        while len(temp) < 10:
            temp = "0" + temp
        return temp


def write_file(obj: dict, filename: str, directory: str = ""):
    if directory:
        os.chdir(directory)
    with open(Path(directory) / filename, "w") as fp:
        json.dump(obj, fp, indent=4)
