import pandas as pd
import json


def load_file(file: str) -> dict:
    """Loads a json file

    Args:
        file (str): The file to load

    Returns:
        dict: The file contents
    """
    with open(file, "r") as f:
        return json.load(f)


def read_submissions(results: dict) -> pd.DataFrame:
    """Reads the submissions file and returns a pandas dataframe

    Args:
        submissions_file (str): The submissions file

    Returns:
        pd.DataFrame: The submissions dataframe
    """
    filings = results["filings"]
    filings = filings["recent"]
    df = pd.DataFrame(filings)
    return df


def read_facts(facts_file: str) -> pd.DataFrame:
    """Reads the facts file and returns a pandas dataframe
    Problem: the facts tags don't line up exactly. more thought needed

    Args:
        facts_file (str): The facts file

    Returns:
        pd.DataFrame: The facts dataframe
    """
    try:
        fp = load_file(facts_file)
        facts = fp["facts"]
        results = {}
        for key, value in facts.items():
            results[key] = pd.DataFrame(value)

    except FileNotFoundError:
        pass
    except KeyError:
        pass

    return pd.read_json(facts_file)
