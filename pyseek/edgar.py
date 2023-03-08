"""Defines the functions for interacting with the SEC Edgar API"""

import json
from typing import List, TypeVar
from pyseek.models import CIK
from pyseek.utils import make_request, download_document

central_index_key = TypeVar("central_index_key", str, int, CIK)


def get_cik_numbers() -> dict:
    """Download all the company ticker information from the SEC"""
    return make_request("https://www.sec.gov/files/company_tickers.json")


def get_cik_number(company_ticker: str) -> List[CIK]:
    """Central Index Key The Central Index Key (CIK) is used on the SEC's computer systems to identify corporations and individual people who have filed disclosure with the SEC.

    Args:
        company_name (str): Name of the company to search for

    Returns:
        List[dict]: List of CIK(title, ticker, cik_str)
    """
    data = make_request("https://www.sec.gov/files/company_tickers.json")
    data = [data[key] for key in data.keys()]
    results = [CIK(**res) for res in data if res["ticker"] == company_ticker]
    if len(results) == 1:
        return results[0]
    elif len(results) == 0:
        raise ValueError("No results found")
    else:
        return results


def get_all_company_submissions(cik: central_index_key) -> dict:
    """Return the entity's current filing history

    This JSON data structure contains metadata such as current name, former name, and stock exchanges and ticker symbols of publicly-traded companies. The object’s property path contains at least one year’s of filing or to 1,000 (whichever is more) of the most recent filings in a compact columnar data array. If the entity has additional filings, files will contain an array of additional JSON files and the date range for the filings each one contains.

    Args:
        cik (central_index_key): CIK, str, int

    Returns:
        dict: Filing history with metadata
    """

    return make_request(f"https://data.sec.gov/submissions/CIK{cik}.json")


def get_all_company_facts(cik: central_index_key) -> dict:
    """Returns all the company concepts data for an entity in a single call

    Args:
        cik (central_index_key): CIK, str, int

    Returns:
        dict: metadata, along with time series of different company concepts
    """
    return make_request(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")


def get_company_concepts_categories(cik: central_index_key) -> List[str]:
    """Get the categories of concepts that are available for a given company

    Args:
        cik (central_index_key): CIK, str, int

    Returns:
        List[str]: list of the categories that are searchable
    """
    cats = get_all_company_facts(cik)
    return cats.get("facts").keys()


def get_company_facts_by_concept(cik: central_index_key, category: str) -> List[str]:
    """The SEC edgar api supports getting just the data relevant to the gaap figures

    Args:
        cik (central_index_key): central index key to look up

    Returns:
        List[str]: list of the us-gaap concepts that are searchable
    """
    facts = get_all_company_facts(cik)
    return facts.get("facts").get(category)


def get_company_fact(fact: str, cik: central_index_key) -> dict:
    """Hte xbrl/companyconcept API returns a given concept for a given entity. This API supports for annual, quarterly and instantaneous data

    Args:
        fact (str): _description_
        cik (central_index_key): _description_

    Returns:
        dict: _description_
    """ """"""
    """The xbrl/frames API aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period requested.
    This API supports for annual, quarterly and instantaneous data"""
    return make_request(f"https:/data.sec.gov/api/xbrl/companyconcept/CIK/{cik}")


def get_frames(fact: str, period: str, unit: str) -> dict:
    return make_request(
        f"https:/data.sec.gov/api/xbrl/frames/{fact}/{unit}/{period}.json"
    )


def download_company_submission(
    cik: central_index_key, accession_number: str, primaryDocument: str
) -> str:
    """Download a company submission

    Args:
        cik (central_index_key): CIK, str, int
        accession_number (str): Accession number of the submission
        primaryDocument (str): Name of the primary document

    Returns:
        str: The submission as a string
    """
    return download_document(cik, accession_number, primaryDocument)


if __name__ == "__main__":
    with open("temporary/tesla_forms.json", "r") as fp:
        data = json.load(fp)

    cik = data["cik"]
    filings = data["filings"]["recent"]
    accession_number = filings["accessionNumber"][6]
    primaryDocument = filings["primaryDocument"][6]

    r = download_company_submission(cik, accession_number, primaryDocument)
    print(r.status_code)
