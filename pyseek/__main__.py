"""Holds the main entry point for the CLI"""

import typer
from typing import Optional
from . import _read, edgar, models, config, utils, setup, submissions
from pyseek import __app_name__, __version__, SUCCESS

app = typer.Typer()
app.add_typer(submissions.app, name="submissions")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def init(
    user_agent: str = typer.Option(
        ...,
        "--user-agent",
        "-u",
        help="User agent for the package. Use the format <name> (<email>)",
        prompt="Please enter a user-agent for browsing SEC EDGAR website",
    ),
    download: bool = typer.Option(
        True,
        " /--download",
        " /-d",
        help="Download company tickers information to configuration directory",
        prompt="Download company tickers information to configuration directory",
    ),
):
    """Initialize the user settings"""
    result = config.init_config(user_agent)
    if result == SUCCESS:
        typer.echo("Configuration file created successfully")
        if download:
            typer.echo(f"Downloading company tickers information")
            tickers = edgar.get_cik_numbers()
            config.create_file(filename="company_tickers.json")
            utils.write_file(
                tickers, "company_tickers.json", directory=setup.CONFIGURATION_DIRECTORY
            )


@app.command("settings")
def api_settings() -> dict:
    """Get the current settings"""
    apisettings = config.get_api_settings()
    print(list(apisettings.items()))


@app.command()
def get_cik(
    ticker: str,
    use_stored: bool = typer.Option(
        True,
        " /--stored",
        " /-s",
        help="Use the stored company ticker files or retrieve a live list from sec website",
    ),
) -> list[models.CIK]:
    """Get the CIK number for a given ticker"""
    if use_stored:
        print(utils.company_from_ticker(ticker))
    else:
        print(edgar.get_cik_number(ticker))


@app.command()
def company_facts(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
    show_concepts_categories: bool = typer.Option(
        False,
        "--concepts",
        "-c",
        help="Print the company concepts categories for the company",
    ),
) -> dict:
    """Get all the company facts for a given company"""
    company = utils.validate_ticker_or_cik(company)
    result = edgar.get_all_company_facts(company.cik_str)
    utils.write_file(result, company.ticker + "_facts.json")
    if show_concepts_categories:
        print(result.get("facts").keys())


@app.command()
def company_concept(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
    concept: str = typer.Argument(..., help="The concept category to retrieve"),
) -> dict:
    """Returns all facts related to a company concept category

    Args:
        company (str, optional): _description_. Defaults to typer.Argument(..., help='CIK number or ticker of the company').
        concept (str, optional): _description_. Defaults to typer.Argument(..., help='The concept category to retrieve').

    Raises:
        typer.BadParameter: _description_

    Returns:
        dict: _description_
    """
    company = utils.validate_ticker_or_cik(company)
    result = edgar.get_company_concept(company.cik_str, concept)
    utils.write_file(result, company.ticker + "_" + concept + ".json")


@app.command(deprecated=True)
def company_concept_categories(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
) -> list:
    """Get all the company concepts categories for a given CIK"""
    company = utils.validate_ticker_or_cik(company)
    print(edgar.get_company_concepts_categories(company.cik_str))


@app.command(deprecated=True)
def company_facts_by_concept(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
    concept: str = typer.Argument(..., help="The concept category to retrieve"),
) -> dict:
    """Returns all facts related to a company concept category

    Args:
        company (str, optional): _description_. Defaults to typer.Argument(..., help='CIK number or ticker of the company').
        concept (str, optional): _description_. Defaults to typer.Argument(..., help='The concept category to retrieve').

    Raises:
        typer.BadParameter: _description_

    Returns:
        dict: _description_
    """
    company = utils.validate_ticker_or_cik(company)
    print(edgar.get_company_facts_by_concept(company.cik_str, concept))


@app.command()
def company_submissions(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
    filename: str = typer.Option(
        None, "--filename", "-f", help="Filename to save the data"
    ),
) -> dict:
    """Get all the company submissions for a given CIK, returns a csv"""
    company = utils.validate_ticker_or_cik(company)
    results = edgar.get_all_company_submissions(company.cik_str)
    # utils.write_file(results, company.ticker + "_submissions.json")
    df = _read.read_submissions(results)

    if not filename:
        filename = f"{company.ticker}_submissions.csv"
    else:
        if not filename.endswith(".csv"):
            filename = filename + ".csv"

    df.to_csv(filename, index=False)


@app.command()
def download_submission(
    cik_number: int = typer.Argument(..., help="CIK number of the company"),
    accession_number: str = typer.Argument(
        ..., help="Accession number of the submission"
    ),
    primaryDocument: str = typer.Argument(
        ..., help="Primary document of the submission"
    ),
    filename: str = typer.Option(
        None,
        "--filename",
        "-f",
        help="The name of the file to create holding the company submission information",
    ),
) -> dict:
    """Download a company submission for a given CIK"""
    if not isinstance(cik_number, int):
        raise typer.BadParameter(
            "CIK number must be an integer, please use the get_cik command to get the CIK number"
        )

    if not filename:
        filename = f"{cik_number}_{accession_number}_{primaryDocument}.txt"

    result = edgar.download_company_submission(
        cik_number, accession_number, primaryDocument
    )
    utils.write_file(result, filename)


if __name__ == "__main__":
    app()
