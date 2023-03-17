"""Holds the utilities for the package"""


import json
from pathlib import Path
from typing import TypeVar

import requests
from typer import BadParameter

from pyseek import config, models, setup

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
        print(f"There was no JSON response for url: {url}")
        print(f"Check the url for errors. If the url is correct, try again later.")
    except requests.ReadTimeout:
        print("the server did not respond in time")


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
    directory: str = None,
):
    if directory:
        filename = Path(directory) / filename
    with open(filename, "w") as fp:
        json.dump(obj, fp, indent=4)


def validate_ticker_or_cik(company: str) -> models.CIK:
    """Validate the ticker or CIK number

    Args:
        company (str): either the company ticker or the company cik number in str format

    Raises:
        typer.BadParameter: _description_
        typer.BadParameter: _description_

    Returns:
        models.CIK: company information with keys "ticker", "name", "cik_str"
    """
    try:
        company = int(company)
        validation = company_from_cik(company)
        if not validation:
            raise BadParameter(f"No results found for CIK {company}")
        return models.CIK(**validation[0])
    except ValueError:
        result = company_from_ticker(company)
        if result:
            return models.CIK(**result[0])
        else:
            raise BadParameter(f"No results found for ticker {company}")


def validate_calendrical_period(period: str) -> str:
    """Validate the calendrical period

    Args:
        period (str): the period to validate

    Raises:
        typer.BadParameter: _description_

    Returns:
        str: the validated period
    """


def validate_submission_record(company: str = None, record: str = None) -> str:
    if not record:
        record = f"{company}_submissions.csv"
    else:
        if not record.endswith(".csv"):
            record = record + ".csv"
    return record
