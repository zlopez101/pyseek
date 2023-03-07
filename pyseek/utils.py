import json
import os
from typing import TypeVar

import requests
from pathlib import Path
from pyseek import models
from pyseek import setup
from pyseek import config


centralIndexKey = TypeVar("centralIndexKey", str, int, models.CIK)


def set_headers() -> dict:
    """Set the headers for the requests call"""
    settings = config.get_api_settings()
    return {"User-Agent": settings["User-Agent"]}


def make_request(url: str, requestTimeout: int = 5) -> dict:
    """Handles all the requests calls for the package

    Args:
        url (str): url to request

    Returns:
        dict: the json returned
    """
    try:
        r = requests.get(url, headers=set_headers(), timeout=requestTimeout)
        r.raise_for_status()
        return r.json()
    except requests.ConnectionError:
        print("there was a connection error")
    except requests.JSONDecodeError:
        print(f"There was a JSON decode error for url: {url}")
        print(f"Check the url for errors. If the url is correct, try again later.")


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


def download_document(
    cik: centralIndexKey, accession_number: str, primaryDocument: str
):
    """Download a company submission

    Args:
        cik (central_index_key): CIK, str, int
        accession_number (str): Accession number of the submission
        primaryDocument (str): Name of the primary document

    Returns:
        str: The submission as a string
    """
    try:
        response = requests.get(
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/{primaryDocument}",
            headers=set_headers(),
        )
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print("Success!")
    return response.text


def write_file(
    obj: dict,
    filename: str,
):
    with open(filename, "w") as fp:
        json.dump(obj, fp, indent=4)
